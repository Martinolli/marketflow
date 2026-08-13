"""Offline approval for future read-only acquisition provider evidence requests."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import (
    acquisition_generation_chain_candidate_operator_review_service as chain_review,
)


ARTIFACT_KIND_ACQUISITION_PROVIDER_EVIDENCE_REQUEST_APPROVED = (
    "ACQUISITION_PROVIDER_EVIDENCE_REQUEST_APPROVED"
)
SCHEMA_VERSION_ACQUISITION_PROVIDER_EVIDENCE_REQUEST_APPROVAL_V1 = (
    "acquisition_provider_evidence_request_approval_v1"
)
ACQUISITION_PROVIDER_EVIDENCE_REQUEST_APPROVED = (
    "ACQUISITION_PROVIDER_EVIDENCE_REQUEST_APPROVED"
)
READ_ONLY_HISTORICAL_MARKET_DATA_ACQUISITION_REQUEST_APPROVAL_ONLY = (
    "READ_ONLY_HISTORICAL_MARKET_DATA_ACQUISITION_REQUEST_APPROVAL_ONLY"
)
OPERATOR_DECISION_APPROVE_ACQUISITION_PROVIDER_EVIDENCE_REQUEST = (
    "APPROVE_ACQUISITION_PROVIDER_EVIDENCE_REQUEST"
)
OPERATOR_ATTESTATION_VERSION_ACQUISITION_PROVIDER_EVIDENCE_REQUEST_APPROVAL_V1 = (
    "acquisition_provider_evidence_request_approval_operator_attestation_v1"
)
REQUIRED_ACQUISITION_PROVIDER_EVIDENCE_REQUEST_APPROVAL_ATTESTATION_PHRASE = (
    "APPROVE ACQUISITION PROVIDER EVIDENCE REQUEST MSFT NVDA AMZN GOOGL META "
    "TSLA JPM XOM JNJ WMT CAT LMT "
    "READ_ONLY_HISTORICAL_MARKET_DATA_ACQUISITION_REQUESTS_ONLY"
)

EXPECTED_ACQUISITION_GENERATION_CHAIN_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    "4df1f99cc3902219a658cb2459353e73b3be12cba22365cfec35c2170a75af3d"
)
EXPECTED_ACQUISITION_GENERATION_CHAIN_CANDIDATE_DIGEST = (
    chain_review.EXPECTED_REVIEWED_ACQUISITION_GENERATION_CHAIN_CANDIDATE_DIGEST
)
EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST = (
    chain_review.candidate_service.EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST
)
EXPECTED_COMBINED_READINESS_REVIEW_PACKAGE_DIGEST = (
    chain_review.candidate_service.EXPECTED_COMBINED_READINESS_REVIEW_PACKAGE_DIGEST
)
EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST = (
    chain_review.candidate_service.EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST
)
EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST = (
    chain_review.candidate_service.EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST
)
EXPECTED_DIVIDEND_EVENT_AUTHORITY_FREEZE_DIGEST = (
    chain_review.candidate_service.EXPECTED_DIVIDEND_EVENT_AUTHORITY_FREEZE_DIGEST
)
EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST = (
    chain_review.candidate_service.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST
)
EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST = (
    chain_review.candidate_service.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST
)
EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST = (
    chain_review.candidate_service.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST
)

TARGET_UNIVERSE = list(chain_review.TARGET_UNIVERSE)
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
NOT_EXECUTED = "NOT_EXECUTED"
NOT_CREATED = "NOT_CREATED"
AUTHORIZED_NOT_EXECUTED = "AUTHORIZED_NOT_EXECUTED"
PLANNED_NOT_GENERATED = chain_review.candidate_service.PLANNED_NOT_GENERATED
RESEARCH_ONLY_NON_ACTIONABLE = (
    chain_review.candidate_service.RESEARCH_ONLY_NON_ACTIONABLE
)
NOT_AUTHORIZED = chain_review.candidate_service.NOT_AUTHORIZED
NOT_ACCEPTED = acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED
PROFITABILITY_NOT_ACCEPTED = acquisition.PROFITABILITY_NOT_ACCEPTED

ACQUISITION_PROVIDER_EVIDENCE_REQUEST_OBJECTIVE = (
    "AUTHORIZE_READ_ONLY_HISTORICAL_MARKET_DATA_ACQUISITION_REQUEST_FOR_EXPANDED_UNIVERSE"
)
ACQUISITION_PROVIDER_EVIDENCE_REQUEST_SCOPE = (
    "READ_ONLY_HISTORICAL_MARKET_DATA_ACQUISITION_REQUESTS_ONLY"
)
ACQUISITION_PROVIDER_EVIDENCE_AUTHORITY_SCOPE = (
    "EVIDENCE_REQUEST_ONLY_NOT_ACQUISITION_GENERATION_AUTHORITY"
)
ACQUISITION_PROVIDER_EVIDENCE_EXECUTION_STATUS = NOT_EXECUTED

READ_ONLY_REQUEST_POLICY = {
    "allowed_future_request_type": ACQUISITION_PROVIDER_EVIDENCE_REQUEST_SCOPE,
    "provider_request_endpoint_plan": (
        "HISTORICAL_AGGREGATES_OR_BARS_ENDPOINT_TO_BE_SELECTED_BY_EXECUTION_SERVICE_OR_FAIL_CLOSED"
    ),
    "api_key_handling": "DO_NOT_STORE_KEYS_OR_PRINT_KEYS",
    "raw_payload_policy": "DO_NOT_COMMIT_RAW_PROVIDER_PAYLOADS",
    "sanitized_status_doc_required": True,
    "rate_limit_policy": "RESPECT_PROVIDER_LIMITS_AND_FAIL_CLOSED",
    "provider_result_authority": "ACQUISITION_EVIDENCE_ONLY_NOT_DATASET_AUTHORITY",
}
PLANNED_ACQUISITION_EVIDENCE_OUTPUT_NAMES = [
    "acquisition_provider_evidence_run_manifest",
    "acquisition_provider_request_receipts_sanitized",
    "acquisition_evidence_results_sanitized",
    "acquisition_failure_reason_inventory",
    "acquisition_data_quality_summary",
    "acquisition_digest_manifest",
    "operator_review_summary",
]
REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS = [
    "operator_confirms_request_scope_read_only_historical_market_data_acquisition_only",
    "operator_confirms_ready_for_acquisition_provider_evidence_execution",
    "operator_confirms_no_provider_requests_made_in_approval",
    "operator_confirms_no_live_provider_transport_enabled",
    "operator_confirms_no_market_data_acquisition_performed",
    "operator_confirms_no_acquisition_generation_authorization",
    "operator_confirms_no_acquisition_generation_execution",
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
    "acquisition_chain_candidate_review_digest_matches_expected",
    "acquisition_chain_candidate_review_has_zero_blockers",
    "acquisition_chain_candidate_digest_matches_expected",
    "corporate_action_authority_approval_digest_bound",
    "combined_readiness_review_digest_bound",
    "split_authority_freeze_digest_bound",
    "dividend_authority_freeze_digest_bound",
    "identity_freeze_digest_bound",
    "target_universe_count_12",
    "target_universe_matches_acquisition_chain_universe",
    "operator_decision_approved",
    "operator_attestation_phrase_matches",
    "operator_confirms_all_source_digests",
    "operator_confirms_request_scope_read_only_acquisition_only",
    "operator_confirms_ready_for_acquisition_provider_evidence_execution",
    "acquisition_provider_request_authorized_true",
    "ready_for_acquisition_provider_evidence_execution_true",
    "provider_requests_made_in_approval_false",
    "live_provider_transport_enabled_in_approval_false",
    "market_data_acquisition_performed_in_approval_false",
    "acquisition_provider_evidence_execution_status_not_executed",
    "acquisition_provider_evidence_results_status_not_created",
    "new_ticker_acquisition_authorized_false",
    "acquisition_generation_authorized_false",
    "acquisition_generation_executed_false",
    "dataset_generation_authorized_false",
    "canonical_dataset_authorized_false",
    "canonical_dataset_candidate_created_false",
    "canonical_dataset_frozen_false",
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
    "planned_outputs_not_generated",
    "planned_outputs_research_only",
    "no_acquisition_execution_artifact_created",
    "no_acquisition_generation_approval_created",
    "no_dataset_generation_authorization_created",
    "no_canonical_dataset_artifact_created",
    "no_registry_approval_created",
    "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created",
    "no_runtime_migration_approval_created",
]

REMAINING_REQUIRED_TASKS = [
    "acquisition_provider_evidence_execution",
    "acquisition_results_review",
    "acquisition_generation_approval_if_required",
    "acquisition_generation_freeze",
    "canonical_dataset_chain_candidate",
    "research_registry_chain",
]


class AcquisitionProviderEvidenceRequestApprovalError(ValueError):
    """Raised when request approval evidence or attestation is invalid."""


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
        raise AcquisitionProviderEvidenceRequestApprovalError(f"{field} mismatch")


def _expect_true(actual: Any, field: str) -> None:
    if actual is not True:
        raise AcquisitionProviderEvidenceRequestApprovalError(f"{field} must be true")


def _expect_false(actual: Any, field: str) -> None:
    if actual is not False:
        raise AcquisitionProviderEvidenceRequestApprovalError(f"{field} must be false")


def _expect_digest(actual: Any, field: str) -> None:
    if not isinstance(actual, str) or len(actual) != 64:
        raise AcquisitionProviderEvidenceRequestApprovalError(f"{field} missing")


def build_acquisition_provider_evidence_request_approval_attestation_v1(
    *,
    operator_reference: str,
    operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str,
    operator_confirms_acquisition_chain_candidate_review_digest: str,
    operator_confirms_acquisition_chain_candidate_digest: str,
    operator_confirms_corporate_action_authority_approval_digest: str,
    operator_confirms_combined_readiness_review_digest: str,
    operator_confirms_split_authority_freeze_digest: str,
    operator_confirms_dividend_authority_freeze_digest: str,
    operator_confirms_identity_freeze_digest: str,
    operator_confirms_target_universe: list[str],
    operator_confirms_target_count: int,
    operator_confirms_request_scope_read_only_historical_market_data_acquisition_only: bool,
    operator_confirms_ready_for_acquisition_provider_evidence_execution: bool,
    operator_confirms_no_provider_requests_made_in_approval: bool,
    operator_confirms_no_live_provider_transport_enabled: bool,
    operator_confirms_no_market_data_acquisition_performed: bool,
    operator_confirms_no_acquisition_generation_authorization: bool,
    operator_confirms_no_acquisition_generation_execution: bool,
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
    operator_decision: str = OPERATOR_DECISION_APPROVE_ACQUISITION_PROVIDER_EVIDENCE_REQUEST,
) -> dict[str, Any]:
    return {name: deepcopy(value) for name, value in locals().items()} | {
        "operator_attestation_version": OPERATOR_ATTESTATION_VERSION_ACQUISITION_PROVIDER_EVIDENCE_REQUEST_APPROVAL_V1
    }


def _expected_digest_confirmations() -> dict[str, str]:
    return {
        "operator_confirms_acquisition_chain_candidate_review_digest": EXPECTED_ACQUISITION_GENERATION_CHAIN_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "operator_confirms_acquisition_chain_candidate_digest": EXPECTED_ACQUISITION_GENERATION_CHAIN_CANDIDATE_DIGEST,
        "operator_confirms_corporate_action_authority_approval_digest": EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST,
        "operator_confirms_combined_readiness_review_digest": EXPECTED_COMBINED_READINESS_REVIEW_PACKAGE_DIGEST,
        "operator_confirms_split_authority_freeze_digest": EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST,
        "operator_confirms_dividend_authority_freeze_digest": EXPECTED_DIVIDEND_EVENT_AUTHORITY_FREEZE_DIGEST,
        "operator_confirms_identity_freeze_digest": EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
    }


def _validate_attestation(attestation: Mapping[str, Any]) -> None:
    if not isinstance(attestation, Mapping):
        raise AcquisitionProviderEvidenceRequestApprovalError("operator_attestation missing")
    expected = {
        "operator_decision": OPERATOR_DECISION_APPROVE_ACQUISITION_PROVIDER_EVIDENCE_REQUEST,
        "operator_attestation_phrase": REQUIRED_ACQUISITION_PROVIDER_EVIDENCE_REQUEST_APPROVAL_ATTESTATION_PHRASE,
        "operator_attestation_version": OPERATOR_ATTESTATION_VERSION_ACQUISITION_PROVIDER_EVIDENCE_REQUEST_APPROVAL_V1,
        "operator_confirms_target_universe": TARGET_UNIVERSE,
        "operator_confirms_target_count": 12,
        **_expected_digest_confirmations(),
    }
    for field, value in expected.items():
        _expect(attestation.get(field), value, field)
    for field in REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS:
        _expect_true(attestation.get(field), field)
    for field in ("operator_reference", "operator_attestation_timestamp_utc"):
        if not isinstance(attestation.get(field), str) or not attestation[field].strip():
            raise AcquisitionProviderEvidenceRequestApprovalError(f"{field} required")


def _source_review(source: dict[str, Any] | None) -> dict[str, Any]:
    package = (
        chain_review.build_acquisition_generation_chain_candidate_review_package_v1()
        if source is None
        else deepcopy(source)
    )
    validation = (
        chain_review.validate_acquisition_generation_chain_candidate_review_package_v1(
            package
        )
    )
    _expect(
        validation.get("acquisition_generation_chain_candidate_review_package_digest"),
        EXPECTED_ACQUISITION_GENERATION_CHAIN_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "source review digest",
    )
    _expect(validation.get("blocker_count"), 0, "source review blocker_count")
    return package


def per_ticker_acquisition_provider_evidence_request_approval_digest_v1(
    entry: dict[str, Any],
) -> str:
    payload = deepcopy(entry)
    payload.pop("per_ticker_acquisition_provider_evidence_request_approval_digest", None)
    return semantic_digest(payload)


def _per_ticker_entries(source: dict[str, Any]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for reviewed in source["per_ticker_acquisition_generation_chain_review_entries"]:
        entry = {
            "ticker": reviewed["ticker"],
            "acquisition_generation_chain_status": reviewed[
                "acquisition_generation_chain_status"
            ],
            "acquisition_generation_chain_review_status": reviewed[
                "acquisition_generation_chain_review_status"
            ],
            "acquisition_provider_request_status": AUTHORIZED_NOT_EXECUTED,
            "acquisition_provider_evidence_execution_status": NOT_EXECUTED,
            "acquisition_provider_evidence_results_status": NOT_CREATED,
            "new_ticker_acquisition_authorized": False,
            "acquisition_generation_authorized": False,
            "acquisition_generation_executed": False,
            "market_data_acquisition_status": NOT_EXECUTED,
            "dataset_generation_authorized": False,
            "canonical_dataset_authorized": False,
            "registry_approval_created": False,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "source_per_ticker_acquisition_generation_chain_candidate_digest": reviewed[
                "per_ticker_acquisition_generation_chain_candidate_digest"
            ],
            "source_per_ticker_acquisition_generation_chain_review_digest": reviewed[
                "per_ticker_acquisition_generation_chain_review_digest"
            ],
        }
        entry["per_ticker_acquisition_provider_evidence_request_approval_digest"] = (
            per_ticker_acquisition_provider_evidence_request_approval_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _planned_outputs() -> list[dict[str, str]]:
    return [
        {
            "output_name": name,
            "generation_status": PLANNED_NOT_GENERATED,
            "actionability": RESEARCH_ONLY_NON_ACTIONABLE,
        }
        for name in PLANNED_ACQUISITION_EVIDENCE_OUTPUT_NAMES
    ]


def _base_artifact(
    source: dict[str, Any], attestation: Mapping[str, Any]
) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_ACQUISITION_PROVIDER_EVIDENCE_REQUEST_APPROVED,
        "schema_version": SCHEMA_VERSION_ACQUISITION_PROVIDER_EVIDENCE_REQUEST_APPROVAL_V1,
        "approval_status": ACQUISITION_PROVIDER_EVIDENCE_REQUEST_APPROVED,
        "approval_scope": READ_ONLY_HISTORICAL_MARKET_DATA_ACQUISITION_REQUEST_APPROVAL_ONLY,
        "created_offline": True,
        "provider_requests_made_in_approval": False,
        "live_provider_transport_enabled_in_approval": False,
        "market_data_acquisition_performed_in_approval": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "acquisition_generation_chain_candidate_created": True,
        "acquisition_generation_chain_candidate_review_created": True,
        "acquisition_provider_request_authorized": True,
        "ready_for_acquisition_provider_evidence_execution": True,
        "acquisition_provider_evidence_executed": False,
        "acquisition_provider_evidence_results_created": False,
        "new_ticker_acquisition_authorized": False,
        "acquisition_generation_authorized": False,
        "acquisition_generation_executed": False,
        "acquisition_generation_results_created": False,
        "acquisition_generation_frozen": False,
        "dataset_generation_authorized": False,
        "canonical_dataset_authorized": False,
        "canonical_dataset_candidate_created": False,
        "canonical_dataset_frozen": False,
        "registry_approval_created": False,
        "corporate_action_authority_created": True,
        "corporate_action_authority_approved": True,
        "corporate_action_authority_scope": chain_review.candidate_service.authority.CORPORATE_ACTION_AUTHORITY_ONLY,
        "split_event_authority_created": True,
        "split_event_authority_frozen": True,
        "split_event_authority_scope": chain_review.candidate_service.authority.readiness.split_freeze.SPLIT_EVENT_AUTHORITY_ONLY,
        "dividend_event_authority_created": True,
        "dividend_event_authority_frozen": True,
        "dividend_event_authority_scope": chain_review.candidate_service.authority.readiness.dividend_freeze.DIVIDEND_EVENT_AUTHORITY_ONLY,
        "identity_authority_created": True,
        "identity_authority_frozen": True,
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
        "acquisition_generation_chain_candidate_review_package_digest": EXPECTED_ACQUISITION_GENERATION_CHAIN_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "acquisition_generation_chain_candidate_digest": EXPECTED_ACQUISITION_GENERATION_CHAIN_CANDIDATE_DIGEST,
        "corporate_action_authority_approval_digest": EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST,
        "combined_split_dividend_corporate_action_readiness_review_package_digest": EXPECTED_COMBINED_READINESS_REVIEW_PACKAGE_DIGEST,
        "corporate_action_authority_plan_approval_digest": EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST,
        "split_event_authority_freeze_digest": EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST,
        "dividend_event_authority_freeze_digest": EXPECTED_DIVIDEND_EVENT_AUTHORITY_FREEZE_DIGEST,
        "post_identity_freeze_registry_inventory_approval_digest": EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST,
        "identity_authority_freeze_digest": EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
        "ticker_universe_selection_approval_digest": EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST,
        "source_acquisition_chain_review_blocker_count": source["review_summary"][
            "blocker_count"
        ],
        "target_universe": list(TARGET_UNIVERSE),
        "target_universe_count": 12,
        "acquisition_provider_evidence_request_objective": ACQUISITION_PROVIDER_EVIDENCE_REQUEST_OBJECTIVE,
        "acquisition_provider_evidence_request_scope": ACQUISITION_PROVIDER_EVIDENCE_REQUEST_SCOPE,
        "acquisition_provider_evidence_authority_scope": ACQUISITION_PROVIDER_EVIDENCE_AUTHORITY_SCOPE,
        "acquisition_provider_evidence_execution_status": ACQUISITION_PROVIDER_EVIDENCE_EXECUTION_STATUS,
        "acquisition_provider_evidence_results_status": NOT_CREATED,
        "read_only_request_policy": deepcopy(READ_ONLY_REQUEST_POLICY),
        "per_ticker_acquisition_provider_evidence_request_approvals": _per_ticker_entries(
            source
        ),
        "planned_outputs": _planned_outputs(),
        "planned_outputs_status": PLANNED_NOT_GENERATED,
        "planned_outputs_label": RESEARCH_ONLY_NON_ACTIONABLE,
        "operator_attestation": deepcopy(dict(attestation)),
        "acquisition_execution_artifact_created": False,
        "acquisition_generation_approval_created": False,
        "dataset_generation_authorization_created": False,
        "canonical_dataset_artifact_created": False,
        "registry_approval_artifact_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
    }


def _checklist(artifact: dict[str, Any]) -> list[dict[str, Any]]:
    operator = artifact["operator_attestation"]
    outputs = artifact["planned_outputs"]
    values: dict[str, tuple[Any, Any]] = {
        "acquisition_chain_candidate_review_digest_matches_expected": (EXPECTED_ACQUISITION_GENERATION_CHAIN_CANDIDATE_REVIEW_PACKAGE_DIGEST, artifact.get("acquisition_generation_chain_candidate_review_package_digest")),
        "acquisition_chain_candidate_review_has_zero_blockers": (0, artifact.get("source_acquisition_chain_review_blocker_count")),
        "acquisition_chain_candidate_digest_matches_expected": (EXPECTED_ACQUISITION_GENERATION_CHAIN_CANDIDATE_DIGEST, artifact.get("acquisition_generation_chain_candidate_digest")),
        "corporate_action_authority_approval_digest_bound": (EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST, artifact.get("corporate_action_authority_approval_digest")),
        "combined_readiness_review_digest_bound": (EXPECTED_COMBINED_READINESS_REVIEW_PACKAGE_DIGEST, artifact.get("combined_split_dividend_corporate_action_readiness_review_package_digest")),
        "split_authority_freeze_digest_bound": (EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST, artifact.get("split_event_authority_freeze_digest")),
        "dividend_authority_freeze_digest_bound": (EXPECTED_DIVIDEND_EVENT_AUTHORITY_FREEZE_DIGEST, artifact.get("dividend_event_authority_freeze_digest")),
        "identity_freeze_digest_bound": (EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST, artifact.get("identity_authority_freeze_digest")),
        "target_universe_count_12": (12, artifact.get("target_universe_count")),
        "target_universe_matches_acquisition_chain_universe": (TARGET_UNIVERSE, artifact.get("target_universe")),
        "operator_decision_approved": (OPERATOR_DECISION_APPROVE_ACQUISITION_PROVIDER_EVIDENCE_REQUEST, operator.get("operator_decision")),
        "operator_attestation_phrase_matches": (REQUIRED_ACQUISITION_PROVIDER_EVIDENCE_REQUEST_APPROVAL_ATTESTATION_PHRASE, operator.get("operator_attestation_phrase")),
        "operator_confirms_all_source_digests": (True, all(operator.get(field) == value for field, value in _expected_digest_confirmations().items())),
        "operator_confirms_request_scope_read_only_acquisition_only": (True, operator.get("operator_confirms_request_scope_read_only_historical_market_data_acquisition_only")),
        "operator_confirms_ready_for_acquisition_provider_evidence_execution": (True, operator.get("operator_confirms_ready_for_acquisition_provider_evidence_execution")),
        "acquisition_provider_request_authorized_true": (True, artifact.get("acquisition_provider_request_authorized")),
        "ready_for_acquisition_provider_evidence_execution_true": (True, artifact.get("ready_for_acquisition_provider_evidence_execution")),
        "acquisition_provider_evidence_execution_status_not_executed": (NOT_EXECUTED, artifact.get("acquisition_provider_evidence_execution_status")),
        "acquisition_provider_evidence_results_status_not_created": (NOT_CREATED, artifact.get("acquisition_provider_evidence_results_status")),
        "predictive_usefulness_not_accepted": (NOT_ACCEPTED, artifact.get("predictive_usefulness")),
        "profitability_not_accepted": (PROFITABILITY_NOT_ACCEPTED, artifact.get("profitability")),
        "runtime_use_not_authorized": (NOT_AUTHORIZED, artifact.get("runtime_use")),
        "strategy_use_not_authorized": (NOT_AUTHORIZED, artifact.get("strategy_use")),
        "paper_trading_not_authorized": (NOT_AUTHORIZED, artifact.get("paper_trading")),
        "broker_execution_not_authorized": (NOT_AUTHORIZED, artifact.get("broker_execution")),
        "planned_outputs_not_generated": (True, bool(outputs) and all(row.get("generation_status") == PLANNED_NOT_GENERATED for row in outputs)),
        "planned_outputs_research_only": (True, bool(outputs) and all(row.get("actionability") == RESEARCH_ONLY_NON_ACTIONABLE for row in outputs)),
    }
    false_checks = {
        "provider_requests_made_in_approval_false": "provider_requests_made_in_approval",
        "live_provider_transport_enabled_in_approval_false": "live_provider_transport_enabled_in_approval",
        "market_data_acquisition_performed_in_approval_false": "market_data_acquisition_performed_in_approval",
        "new_ticker_acquisition_authorized_false": "new_ticker_acquisition_authorized",
        "acquisition_generation_authorized_false": "acquisition_generation_authorized",
        "acquisition_generation_executed_false": "acquisition_generation_executed",
        "dataset_generation_authorized_false": "dataset_generation_authorized",
        "canonical_dataset_authorized_false": "canonical_dataset_authorized",
        "canonical_dataset_candidate_created_false": "canonical_dataset_candidate_created",
        "canonical_dataset_frozen_false": "canonical_dataset_frozen",
        "registry_approval_created_false": "registry_approval_created",
        "additional_predictive_evidence_execution_authorized_false": "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed_false": "additional_predictive_evidence_executed",
        "predictive_experiment_rerun_authorized_false": "predictive_experiment_rerun_authorized",
        "new_strategy_scoring_performed_false": "new_strategy_scoring_performed",
        "trade_recommendations_generated_false": "trade_recommendations_generated",
        "runtime_migration_approved_false": "runtime_migration_approved",
        "automatic_stitching_false": "automatic_stitching",
        "no_acquisition_execution_artifact_created": "acquisition_execution_artifact_created",
        "no_acquisition_generation_approval_created": "acquisition_generation_approval_created",
        "no_dataset_generation_authorization_created": "dataset_generation_authorization_created",
        "no_canonical_dataset_artifact_created": "canonical_dataset_artifact_created",
        "no_registry_approval_created": "registry_approval_artifact_created",
        "no_predictive_usefulness_acceptance_artifact_created": "predictive_usefulness_acceptance_artifact_created",
        "no_profitability_acceptance_created": "profitability_acceptance_created",
        "no_runtime_migration_approval_created": "runtime_migration_approval_created",
    }
    values.update(
        {check_id: (False, artifact.get(field)) for check_id, field in false_checks.items()}
    )
    return [_check(check_id, *values[check_id]) for check_id in REQUIRED_APPROVAL_CHECK_IDS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [row for row in checklist if row["status"] != PASS]
    return {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row["severity"] == BLOCKER for row in failed),
        "acquisition_provider_request_authorized_by_operator": not failed,
        "ready_for_acquisition_provider_evidence_execution": not failed,
        "provider_requests_made_in_approval": False,
        "market_data_acquisition_performed": False,
        "acquisition_authorized": False,
        "acquisition_generation_authorized": False,
        "acquisition_generation_executed": False,
        "dataset_generation_authorized": False,
        "canonical_dataset_authorized": False,
        "registry_approval_created": False,
        "additional_predictive_evidence_execution_authorized": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def acquisition_provider_evidence_request_approval_digest_v1(
    artifact: dict[str, Any],
) -> str:
    payload = deepcopy(artifact)
    payload.pop("acquisition_provider_evidence_request_approval_digest", None)
    return semantic_digest(payload)


def build_acquisition_provider_evidence_request_approved_v1(
    *,
    acquisition_chain_review_package: dict[str, Any] | None = None,
    operator_attestation: dict[str, Any],
) -> dict[str, Any]:
    source = _source_review(acquisition_chain_review_package)
    _validate_attestation(operator_attestation)
    artifact = _base_artifact(source, operator_attestation)
    artifact["approval_checklist"] = _checklist(artifact)
    artifact["approval_summary"] = _summary(artifact["approval_checklist"])
    artifact["acquisition_provider_evidence_request_approval_digest"] = (
        acquisition_provider_evidence_request_approval_digest_v1(artifact)
    )
    validate_acquisition_provider_evidence_request_approved_v1(artifact)
    return artifact


def _validate_per_ticker(artifact: dict[str, Any]) -> None:
    entries = artifact.get("per_ticker_acquisition_provider_evidence_request_approvals")
    if not isinstance(entries, list) or len(entries) != 12:
        raise AcquisitionProviderEvidenceRequestApprovalError(
            "per_ticker entries mismatch"
        )
    _expect([row.get("ticker") for row in entries], TARGET_UNIVERSE, "per_ticker tickers")
    for row in entries:
        expected = {
            "acquisition_generation_chain_status": chain_review.candidate_service.PLANNED_READY_FOR_OPERATOR_REVIEW,
            "acquisition_generation_chain_review_status": chain_review.READY_FOR_OPERATOR_ASSESSMENT,
            "acquisition_provider_request_status": AUTHORIZED_NOT_EXECUTED,
            "acquisition_provider_evidence_execution_status": NOT_EXECUTED,
            "acquisition_provider_evidence_results_status": NOT_CREATED,
            "new_ticker_acquisition_authorized": False,
            "acquisition_generation_authorized": False,
            "acquisition_generation_executed": False,
            "market_data_acquisition_status": NOT_EXECUTED,
            "dataset_generation_authorized": False,
            "canonical_dataset_authorized": False,
            "registry_approval_created": False,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
        }
        for field, value in expected.items():
            _expect(row.get(field), value, f"{row['ticker']}.{field}")
        _expect_digest(
            row.get("source_per_ticker_acquisition_generation_chain_candidate_digest"),
            f"{row['ticker']}.source candidate digest",
        )
        _expect_digest(
            row.get("source_per_ticker_acquisition_generation_chain_review_digest"),
            f"{row['ticker']}.source review digest",
        )
        digest = row.get(
            "per_ticker_acquisition_provider_evidence_request_approval_digest"
        )
        _expect_digest(digest, f"{row['ticker']}.approval digest")
        _expect(
            digest,
            per_ticker_acquisition_provider_evidence_request_approval_digest_v1(row),
            f"{row['ticker']}.approval digest",
        )


def validate_acquisition_provider_evidence_request_approved_v1(
    approved_artifact: dict[str, Any],
) -> dict[str, Any]:
    if not isinstance(approved_artifact, dict):
        raise AcquisitionProviderEvidenceRequestApprovalError(
            "approved_artifact must be an object"
        )
    expected = {
        "artifact_kind": ARTIFACT_KIND_ACQUISITION_PROVIDER_EVIDENCE_REQUEST_APPROVED,
        "schema_version": SCHEMA_VERSION_ACQUISITION_PROVIDER_EVIDENCE_REQUEST_APPROVAL_V1,
        "approval_status": ACQUISITION_PROVIDER_EVIDENCE_REQUEST_APPROVED,
        "approval_scope": READ_ONLY_HISTORICAL_MARKET_DATA_ACQUISITION_REQUEST_APPROVAL_ONLY,
        "acquisition_generation_chain_candidate_review_package_digest": EXPECTED_ACQUISITION_GENERATION_CHAIN_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "acquisition_generation_chain_candidate_digest": EXPECTED_ACQUISITION_GENERATION_CHAIN_CANDIDATE_DIGEST,
        "corporate_action_authority_approval_digest": EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST,
        "combined_split_dividend_corporate_action_readiness_review_package_digest": EXPECTED_COMBINED_READINESS_REVIEW_PACKAGE_DIGEST,
        "split_event_authority_freeze_digest": EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST,
        "dividend_event_authority_freeze_digest": EXPECTED_DIVIDEND_EVENT_AUTHORITY_FREEZE_DIGEST,
        "identity_authority_freeze_digest": EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
        "target_universe": TARGET_UNIVERSE,
        "target_universe_count": 12,
        "acquisition_provider_evidence_request_objective": ACQUISITION_PROVIDER_EVIDENCE_REQUEST_OBJECTIVE,
        "acquisition_provider_evidence_request_scope": ACQUISITION_PROVIDER_EVIDENCE_REQUEST_SCOPE,
        "acquisition_provider_evidence_authority_scope": ACQUISITION_PROVIDER_EVIDENCE_AUTHORITY_SCOPE,
        "acquisition_provider_evidence_execution_status": NOT_EXECUTED,
        "acquisition_provider_evidence_results_status": NOT_CREATED,
        "read_only_request_policy": READ_ONLY_REQUEST_POLICY,
        "planned_outputs_status": PLANNED_NOT_GENERATED,
        "planned_outputs_label": RESEARCH_ONLY_NON_ACTIONABLE,
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
        "created_offline",
        "acquisition_generation_chain_candidate_created",
        "acquisition_generation_chain_candidate_review_created",
        "acquisition_provider_request_authorized",
        "ready_for_acquisition_provider_evidence_execution",
        "corporate_action_authority_created",
        "corporate_action_authority_approved",
        "split_event_authority_created",
        "split_event_authority_frozen",
        "dividend_event_authority_created",
        "dividend_event_authority_frozen",
        "identity_authority_created",
        "identity_authority_frozen",
        "research_only",
    )
    false_fields = (
        "provider_requests_made_in_approval",
        "live_provider_transport_enabled_in_approval",
        "market_data_acquisition_performed_in_approval",
        "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
        "acquisition_provider_evidence_executed",
        "acquisition_provider_evidence_results_created",
        "new_ticker_acquisition_authorized",
        "acquisition_generation_authorized",
        "acquisition_generation_executed",
        "acquisition_generation_results_created",
        "acquisition_generation_frozen",
        "dataset_generation_authorized",
        "canonical_dataset_authorized",
        "canonical_dataset_candidate_created",
        "canonical_dataset_frozen",
        "registry_approval_created",
        "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed",
        "predictive_experiment_rerun_authorized",
        "predictive_experiment_rerun_performed",
        "feature_matrix_regeneration_performed",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
        "runtime_migration_approved",
        "runtime_migration_active",
        "automatic_stitching",
        "acquisition_execution_artifact_created",
        "acquisition_generation_approval_created",
        "dataset_generation_authorization_created",
        "canonical_dataset_artifact_created",
        "registry_approval_artifact_created",
        "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_created",
        "runtime_migration_approval_created",
    )
    for field in true_fields:
        _expect_true(approved_artifact.get(field), field)
    for field in false_fields:
        _expect_false(approved_artifact.get(field), field)
    _validate_attestation(approved_artifact.get("operator_attestation", {}))
    _validate_per_ticker(approved_artifact)
    outputs = approved_artifact.get("planned_outputs")
    if not isinstance(outputs, list) or len(outputs) != 7:
        raise AcquisitionProviderEvidenceRequestApprovalError("planned_outputs mismatch")
    if any(row.get("generation_status") != PLANNED_NOT_GENERATED for row in outputs):
        raise AcquisitionProviderEvidenceRequestApprovalError("planned output generated")
    if any(row.get("actionability") != RESEARCH_ONLY_NON_ACTIONABLE for row in outputs):
        raise AcquisitionProviderEvidenceRequestApprovalError("planned output actionable")
    checklist = approved_artifact.get("approval_checklist")
    if not isinstance(checklist, list):
        raise AcquisitionProviderEvidenceRequestApprovalError("approval_checklist missing")
    _expect(
        [row.get("check_id") for row in checklist],
        REQUIRED_APPROVAL_CHECK_IDS,
        "approval checklist",
    )
    if any(row.get("status") != PASS for row in checklist):
        raise AcquisitionProviderEvidenceRequestApprovalError("approval checklist failed")
    _expect(approved_artifact.get("approval_summary"), _summary(checklist), "approval_summary")
    digest = approved_artifact.get(
        "acquisition_provider_evidence_request_approval_digest"
    )
    _expect_digest(digest, "approval digest")
    _expect(
        digest,
        acquisition_provider_evidence_request_approval_digest_v1(approved_artifact),
        "approval digest",
    )
    return {
        "status": "ACQUISITION_PROVIDER_EVIDENCE_REQUEST_APPROVED_VALID",
        "artifact_kind": approved_artifact["artifact_kind"],
        "approval_status": approved_artifact["approval_status"],
        "approval_scope": approved_artifact["approval_scope"],
        "acquisition_provider_evidence_request_approval_digest": digest,
        **{
            key: approved_artifact["approval_summary"][key]
            for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")
        },
    }


def build_acquisition_provider_evidence_request_approved_markdown_v1(
    approved_artifact: dict[str, Any],
) -> str:
    validation = validate_acquisition_provider_evidence_request_approved_v1(
        approved_artifact
    )
    lines = [
        "# MarketFlow Acquisition Provider Evidence Request Approval Status",
        "",
        "## Title",
        "- Acquisition Provider Request Approval Ceremony v1.",
        "",
        "## Approved Acquisition Provider Evidence Request",
        f"- Artifact/status: `{approved_artifact['artifact_kind']}` / `{approved_artifact['approval_status']}`.",
        f"- Approval digest: `{validation['acquisition_provider_evidence_request_approval_digest']}`.",
        "",
        "## Operator Attestation",
        f"- Decision/reference: `{approved_artifact['operator_attestation']['operator_decision']}` / `{approved_artifact['operator_attestation']['operator_reference']}`.",
        "",
        "## Source Acquisition Chain Candidate Review",
        f"- Review digest: `{approved_artifact['acquisition_generation_chain_candidate_review_package_digest']}`.",
        "",
        "## Source Corporate-Action Authority Approval",
        f"- Approval digest: `{approved_artifact['corporate_action_authority_approval_digest']}`.",
        "",
        "## Target Universe",
        "- " + ", ".join(f"`{ticker}`" for ticker in TARGET_UNIVERSE),
        "",
        "## Approval Scope",
        f"- `{approved_artifact['approval_scope']}`.",
        "",
        "## Read-Only Provider Request Boundary",
        "- A future read-only request is authorized; no request was made in this ceremony.",
        "",
        "## Acquisition Execution Boundary",
        "- Provider evidence and acquisition generation remain not executed and not authorized respectively.",
        "",
        "## Dataset Boundary",
        "- Dataset generation remains not authorized.",
        "",
        "## Canonical Dataset Boundary",
        "- No canonical dataset candidate, authorization, or freeze was created.",
        "",
        "## Registry Boundary",
        "- No registry approval was created.",
        "",
        "## Predictive/Profitability Boundary",
        "- Predictive usefulness and profitability remain not accepted.",
        "",
        "## Runtime Boundary",
        "- Runtime, strategy, paper trading, and broker execution remain not authorized.",
        "",
        "## Approval Checklist Summary",
        f"- Total/passed/failed/blockers: `{validation['total_checks']} / {validation['passed_checks']} / {validation['failed_checks']} / {validation['blocker_count']}`.",
        "",
        "## Remaining Required Tasks",
    ]
    lines.extend(f"- `{task}`." for task in REMAINING_REQUIRED_TASKS)
    lines.extend(
        [
            "",
            "## Guardrails",
            "- No provider request, market-data acquisition, dataset generation, predictive execution, or runtime activation occurred.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_acquisition_provider_evidence_request_approved_v1(
    output_dir: str | Path,
    *,
    acquisition_chain_review_package: dict[str, Any] | None = None,
    operator_attestation: dict[str, Any],
) -> dict[str, Any]:
    artifact = build_acquisition_provider_evidence_request_approved_v1(
        acquisition_chain_review_package=acquisition_chain_review_package,
        operator_attestation=operator_attestation,
    )
    output_path = Path(output_dir)
    json_path = output_path / "acquisition_provider_evidence_request_approved_v1.json"
    markdown_path = output_path / "acquisition_provider_evidence_request_approved_v1.md"
    if json_path.exists() or markdown_path.exists():
        raise AcquisitionProviderEvidenceRequestApprovalError(
            "acquisition provider request approval output already exists"
        )
    output_path.mkdir(parents=True, exist_ok=True)
    json_path.write_bytes(canonical_json_bytes(artifact))
    markdown_path.write_text(
        build_acquisition_provider_evidence_request_approved_markdown_v1(artifact),
        encoding="utf-8",
    )
    return {
        "artifact": artifact,
        "validation": validate_acquisition_provider_evidence_request_approved_v1(
            artifact
        ),
        "json_path": json_path.as_posix(),
        "markdown_path": markdown_path.as_posix(),
    }
