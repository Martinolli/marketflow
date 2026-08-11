"""Offline approval ceremony for future read-only split provider evidence requests."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import (
    dividend_event_authority_candidate_operator_review_service as dividend_review,
)
from marketflow.services import (
    split_event_authority_candidate_operator_review_service as split_review,
)


ARTIFACT_KIND_SPLIT_PROVIDER_EVIDENCE_REQUEST_APPROVED = (
    "SPLIT_EVENT_PROVIDER_EVIDENCE_REQUEST_APPROVED"
)
SCHEMA_VERSION_SPLIT_PROVIDER_EVIDENCE_REQUEST_APPROVAL_V1 = (
    "split_event_provider_evidence_request_approval_v1"
)
SPLIT_PROVIDER_EVIDENCE_REQUEST_APPROVED = (
    "SPLIT_EVENT_PROVIDER_EVIDENCE_REQUEST_APPROVED"
)
READ_ONLY_SPLIT_EVENT_EVIDENCE_REQUEST_APPROVAL_ONLY = (
    "READ_ONLY_SPLIT_EVENT_EVIDENCE_REQUEST_APPROVAL_ONLY"
)
OPERATOR_DECISION_APPROVE_SPLIT_PROVIDER_EVIDENCE_REQUEST = (
    "APPROVE_SPLIT_PROVIDER_EVIDENCE_REQUEST"
)
OPERATOR_ATTESTATION_VERSION_V1 = (
    "split_provider_evidence_request_approval_operator_attestation_v1"
)
REQUIRED_SPLIT_PROVIDER_EVIDENCE_REQUEST_APPROVAL_ATTESTATION_PHRASE = (
    "APPROVE SPLIT PROVIDER EVIDENCE REQUEST MSFT NVDA AMZN GOOGL META TSLA JPM "
    "XOM JNJ WMT CAT LMT READ_ONLY_SPLIT_EVENT_EVIDENCE_REQUESTS_ONLY"
)

SPLIT_PROVIDER_EVIDENCE_REQUEST_OBJECTIVE = (
    "AUTHORIZE_READ_ONLY_SPLIT_EVENT_PROVIDER_EVIDENCE_REQUEST_FOR_EXPANDED_UNIVERSE"
)
SPLIT_PROVIDER_EVIDENCE_REQUEST_SCOPE = "READ_ONLY_SPLIT_EVENT_EVIDENCE_REQUESTS_ONLY"
SPLIT_PROVIDER_EVIDENCE_AUTHORITY_SCOPE = (
    "EVIDENCE_REQUEST_ONLY_NOT_SPLIT_AUTHORITY"
)
AUTHORIZED_NOT_EXECUTED = "AUTHORIZED_NOT_EXECUTED"
NOT_EXECUTED = "NOT_EXECUTED"
NOT_CREATED = "NOT_CREATED"
PLANNED_NOT_GENERATED = "PLANNED_NOT_GENERATED"
RESEARCH_ONLY_NON_ACTIONABLE = "RESEARCH_ONLY_NON_ACTIONABLE"

EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    "5f59edb21ab0e800aa714cfca41f3fe2b155f012ea7cc6c4c4c382146303c95a"
)
EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_DIGEST = (
    split_review.EXPECTED_REVIEWED_SPLIT_EVENT_AUTHORITY_CANDIDATE_DIGEST
)
EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    "cf120d55beaa22f1fbd4f27d9a7a6539583e5cd67f3d0ffe5a186f318f27a104"
)
EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_DIGEST = (
    dividend_review.EXPECTED_REVIEWED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_DIGEST
)
EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST = (
    split_review.candidate_service.EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST
)
EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    split_review.candidate_service.EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST
)
EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_DIGEST = (
    split_review.candidate_service.EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_DIGEST
)
EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST = (
    split_review.candidate_service.approval.review.plan.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST
)
EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST = (
    split_review.candidate_service.approval.review.plan.approval_service.review_service.candidate_service.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST
)
EXPECTED_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_DIGEST = (
    split_review.candidate_service.approval.review.plan.approval_service.review_service.candidate_service.freeze_service.EXPECTED_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_DIGEST
)
EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST = (
    split_review.candidate_service.approval.review.plan.approval_service.review_service.candidate_service.freeze_service.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST
)

PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
INFO = "INFO"

VALIDATION_TARGET_UNIVERSE = list(split_review.VALIDATION_TARGET_UNIVERSE)

READ_ONLY_REQUEST_POLICY = {
    "allowed_future_request_type": "READ_ONLY_SPLIT_EVENT_EVIDENCE_REQUESTS_ONLY",
    "provider_request_endpoint_plan": (
        "SPLIT_EVENT_ENDPOINT_TO_BE_SELECTED_BY_EXECUTION_SERVICE_OR_FAIL_CLOSED"
    ),
    "api_key_handling": "DO_NOT_STORE_KEYS_OR_PRINT_KEYS",
    "raw_payload_policy": "DO_NOT_COMMIT_RAW_PROVIDER_PAYLOADS",
    "sanitized_status_doc_required": True,
    "rate_limit_policy": "RESPECT_PROVIDER_LIMITS_AND_FAIL_CLOSED",
    "provider_result_authority": "SPLIT_EVENT_EVIDENCE_ONLY_NOT_SPLIT_AUTHORITY",
}

PLANNED_SPLIT_EVIDENCE_OUTPUT_NAMES = [
    "split_provider_evidence_run_manifest",
    "split_event_provider_request_receipts_sanitized",
    "split_event_results_sanitized",
    "split_event_absence_inventory",
    "split_event_failure_reason_inventory",
    "operator_review_summary",
]

OPERATOR_CONFIRMATION_FIELDS = [
    "operator_confirms_request_scope_read_only_split_event_evidence_only",
    "operator_confirms_ready_for_split_provider_evidence_execution",
    "operator_confirms_no_provider_requests_made_in_approval",
    "operator_confirms_no_live_provider_transport_enabled",
    "operator_confirms_no_split_provider_evidence_executed",
    "operator_confirms_no_split_provider_evidence_results_created",
    "operator_confirms_no_split_event_authority_created",
    "operator_confirms_no_split_event_authority_frozen",
    "operator_confirms_no_dividend_provider_evidence_request_authorized",
    "operator_confirms_no_dividend_event_authority_created",
    "operator_confirms_no_corporate_action_authority_created",
    "operator_confirms_no_acquisition_authority",
    "operator_confirms_no_dataset_generation_authorization",
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

REMAINING_ROADMAP_AFTER_APPROVAL = [
    "Split provider evidence execution.",
    "Split event evidence/results review package.",
    "Split event authority freeze ceremony.",
    "Dividend provider evidence request approval ceremony.",
    "Dividend provider evidence execution.",
    "Dividend event authority freeze ceremony.",
]

REQUIRED_APPROVAL_CHECK_IDS = [
    "split_candidate_review_digest_matches_expected",
    "split_candidate_review_has_zero_blockers",
    "split_candidate_digest_matches_expected",
    "dividend_candidate_review_digest_matches_expected",
    "dividend_candidate_digest_matches_expected",
    "corporate_action_plan_approval_digest_bound",
    "corporate_action_plan_review_digest_bound",
    "corporate_action_plan_candidate_digest_bound",
    "registry_inventory_approval_digest_bound",
    "identity_freeze_digest_bound",
    "live_validation_results_review_digest_bound",
    "ticker_universe_selection_approval_digest_bound",
    "target_universe_count_12",
    "target_universe_matches_expected",
    "approval_scope_read_only_split_evidence_request_only",
    "split_provider_evidence_request_objective_matches",
    "split_provider_evidence_request_scope_matches",
    "split_provider_evidence_authority_scope_evidence_only",
    "split_provider_evidence_execution_status_not_executed",
    "read_only_request_policy_matches",
    "per_ticker_split_provider_request_entries_12",
    "per_ticker_split_candidate_status_ready",
    "per_ticker_split_review_status_ready",
    "per_ticker_request_status_authorized_not_executed",
    "per_ticker_execution_status_not_executed",
    "per_ticker_results_status_not_created",
    "per_ticker_split_authority_not_created",
    "per_ticker_split_freeze_not_frozen",
    "per_ticker_dividend_authority_not_created",
    "per_ticker_corporate_action_authority_false",
    "per_ticker_acquisition_authorized_false",
    "per_ticker_dataset_generation_authorized_false",
    "per_ticker_runtime_use_not_authorized",
    "per_ticker_strategy_use_not_authorized",
    "per_ticker_paper_trading_not_authorized",
    "per_ticker_broker_execution_not_authorized",
    "per_ticker_source_split_candidate_digests_present",
    "per_ticker_source_split_review_digests_present",
    "per_ticker_source_plan_approval_digests_present",
    "per_ticker_request_approval_digests_present",
    "operator_decision_approved",
    "operator_attestation_phrase_matches",
    "operator_split_candidate_review_digest_confirmation_matches",
    "operator_split_candidate_digest_confirmation_matches",
    "operator_dividend_candidate_review_digest_confirmation_matches",
    "operator_corporate_action_plan_approval_digest_confirmation_matches",
    "operator_registry_inventory_approval_digest_confirmation_matches",
    "operator_identity_freeze_digest_confirmation_matches",
    "operator_target_universe_confirmation_matches",
    "operator_target_count_confirmation_matches",
    *OPERATOR_CONFIRMATION_FIELDS,
    "split_provider_evidence_request_authorized_true",
    "ready_for_split_provider_evidence_execution_true",
    "provider_requests_made_in_approval_false",
    "live_provider_transport_enabled_in_approval_false",
    "split_provider_evidence_executed_false",
    "split_provider_evidence_results_created_false",
    "split_event_authority_created_false",
    "split_event_authority_frozen_false",
    "dividend_provider_evidence_request_authorized_false",
    "dividend_provider_evidence_executed_false",
    "dividend_provider_evidence_results_created_false",
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
    "profitability_not_accepted",
    "runtime_migration_approved_false",
    "runtime_use_not_authorized",
    "strategy_use_not_authorized",
    "paper_trading_not_authorized",
    "broker_execution_not_authorized",
    "automatic_stitching_false",
    "planned_outputs_not_generated",
    "planned_outputs_research_only",
    "no_split_provider_evidence_execution_created",
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


class SplitProviderEvidenceRequestApprovalError(ValueError):
    """Raised when the split provider evidence request approval is invalid."""


def _check(
    check_id: str,
    expected: Any,
    actual: Any,
    *,
    severity: str = BLOCKER,
) -> dict[str, Any]:
    status = PASS if actual == expected else FAIL
    return {
        "check_id": check_id,
        "status": status,
        "expected": expected,
        "actual": actual,
        "severity": severity,
        "message": f"{check_id} passed" if status == PASS else f"{check_id} failed",
    }


def _expect(actual: Any, expected: Any, field_name: str) -> None:
    if actual != expected:
        raise SplitProviderEvidenceRequestApprovalError(f"{field_name} mismatch")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise SplitProviderEvidenceRequestApprovalError(f"{field_name} must be true")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise SplitProviderEvidenceRequestApprovalError(f"{field_name} must be false")


def _not_authorized() -> str:
    return split_review.candidate_service.NOT_AUTHORIZED


def _path_text(path: Path) -> str:
    return str(path).replace("\\", "/")


def build_split_provider_evidence_request_approval_attestation_v1(
    *,
    operator_reference: str,
    operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str,
    operator_confirms_split_candidate_review_package_digest: str,
    operator_confirms_split_candidate_digest: str,
    operator_confirms_dividend_candidate_review_package_digest: str,
    operator_confirms_corporate_action_plan_approval_digest: str,
    operator_confirms_registry_inventory_approval_digest: str,
    operator_confirms_identity_freeze_digest: str,
    operator_confirms_target_universe: list[str],
    operator_confirms_target_count: int,
    operator_confirms_request_scope_read_only_split_event_evidence_only: bool,
    operator_confirms_ready_for_split_provider_evidence_execution: bool,
    operator_confirms_no_provider_requests_made_in_approval: bool,
    operator_confirms_no_live_provider_transport_enabled: bool,
    operator_confirms_no_split_provider_evidence_executed: bool,
    operator_confirms_no_split_provider_evidence_results_created: bool,
    operator_confirms_no_split_event_authority_created: bool,
    operator_confirms_no_split_event_authority_frozen: bool,
    operator_confirms_no_dividend_provider_evidence_request_authorized: bool,
    operator_confirms_no_dividend_event_authority_created: bool,
    operator_confirms_no_corporate_action_authority_created: bool,
    operator_confirms_no_acquisition_authority: bool,
    operator_confirms_no_dataset_generation_authorization: bool,
    operator_confirms_no_predictive_usefulness_acceptance: bool,
    operator_confirms_no_profitability_acceptance: bool,
    operator_confirms_no_runtime_migration_approval: bool,
    operator_confirms_no_runtime_activation: bool,
    operator_confirms_no_paper_trading: bool,
    operator_confirms_no_broker_execution: bool,
    operator_confirms_no_trade_recommendations: bool,
    operator_confirms_no_api_key_storage_or_printing: bool,
    operator_confirms_no_raw_payload_commit: bool,
    operator_decision: str = OPERATOR_DECISION_APPROVE_SPLIT_PROVIDER_EVIDENCE_REQUEST,
    operator_attestation_version: str = OPERATOR_ATTESTATION_VERSION_V1,
) -> dict[str, Any]:
    """Build a non-secret operator attestation for split evidence request approval."""
    return {
        "operator_reference": operator_reference,
        "operator_decision": operator_decision,
        "operator_attestation_phrase": operator_attestation_phrase,
        "operator_attestation_timestamp_utc": operator_attestation_timestamp_utc,
        "operator_attestation_version": operator_attestation_version,
        "operator_confirms_split_candidate_review_package_digest": (
            operator_confirms_split_candidate_review_package_digest
        ),
        "operator_confirms_split_candidate_digest": operator_confirms_split_candidate_digest,
        "operator_confirms_dividend_candidate_review_package_digest": (
            operator_confirms_dividend_candidate_review_package_digest
        ),
        "operator_confirms_corporate_action_plan_approval_digest": (
            operator_confirms_corporate_action_plan_approval_digest
        ),
        "operator_confirms_registry_inventory_approval_digest": (
            operator_confirms_registry_inventory_approval_digest
        ),
        "operator_confirms_identity_freeze_digest": operator_confirms_identity_freeze_digest,
        "operator_confirms_target_universe": list(operator_confirms_target_universe),
        "operator_confirms_target_count": operator_confirms_target_count,
        "operator_confirms_request_scope_read_only_split_event_evidence_only": (
            operator_confirms_request_scope_read_only_split_event_evidence_only
        ),
        "operator_confirms_ready_for_split_provider_evidence_execution": (
            operator_confirms_ready_for_split_provider_evidence_execution
        ),
        "operator_confirms_no_provider_requests_made_in_approval": (
            operator_confirms_no_provider_requests_made_in_approval
        ),
        "operator_confirms_no_live_provider_transport_enabled": (
            operator_confirms_no_live_provider_transport_enabled
        ),
        "operator_confirms_no_split_provider_evidence_executed": (
            operator_confirms_no_split_provider_evidence_executed
        ),
        "operator_confirms_no_split_provider_evidence_results_created": (
            operator_confirms_no_split_provider_evidence_results_created
        ),
        "operator_confirms_no_split_event_authority_created": (
            operator_confirms_no_split_event_authority_created
        ),
        "operator_confirms_no_split_event_authority_frozen": (
            operator_confirms_no_split_event_authority_frozen
        ),
        "operator_confirms_no_dividend_provider_evidence_request_authorized": (
            operator_confirms_no_dividend_provider_evidence_request_authorized
        ),
        "operator_confirms_no_dividend_event_authority_created": (
            operator_confirms_no_dividend_event_authority_created
        ),
        "operator_confirms_no_corporate_action_authority_created": (
            operator_confirms_no_corporate_action_authority_created
        ),
        "operator_confirms_no_acquisition_authority": (
            operator_confirms_no_acquisition_authority
        ),
        "operator_confirms_no_dataset_generation_authorization": (
            operator_confirms_no_dataset_generation_authorization
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
        "operator_confirms_no_broker_execution": operator_confirms_no_broker_execution,
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


def _source_split_review_package(review_package: dict[str, Any] | None) -> dict[str, Any]:
    source_review = (
        deepcopy(review_package)
        if review_package is not None
        else split_review.build_split_event_authority_candidate_review_package_v1()
    )
    try:
        validation = split_review.validate_split_event_authority_candidate_review_package_v1(
            source_review
        )
    except split_review.SplitEventAuthorityCandidateReviewPackageError as exc:
        raise SplitProviderEvidenceRequestApprovalError(
            f"source split candidate review package invalid: {exc}"
        ) from exc
    _expect(
        validation["split_event_authority_candidate_review_package_digest"],
        EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "source split_event_authority_candidate_review_package_digest",
    )
    _expect(validation["blocker_count"], 0, "source split review blocker_count")
    return source_review


def _source_dividend_review_package(review_package: dict[str, Any] | None) -> dict[str, Any]:
    source_review = (
        deepcopy(review_package)
        if review_package is not None
        else dividend_review.build_dividend_event_authority_candidate_review_package_v1()
    )
    try:
        validation = dividend_review.validate_dividend_event_authority_candidate_review_package_v1(
            source_review
        )
    except dividend_review.DividendEventAuthorityCandidateReviewPackageError as exc:
        raise SplitProviderEvidenceRequestApprovalError(
            f"source dividend candidate review package invalid: {exc}"
        ) from exc
    _expect(
        validation["dividend_event_authority_candidate_review_package_digest"],
        EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "source dividend_event_authority_candidate_review_package_digest",
    )
    _expect(validation["blocker_count"], 0, "source dividend review blocker_count")
    return source_review


def _planned_outputs() -> list[dict[str, Any]]:
    return [
        {
            "output_name": output_name,
            "generation_status": PLANNED_NOT_GENERATED,
            "generated": False,
            "actionability": RESEARCH_ONLY_NON_ACTIONABLE,
        }
        for output_name in PLANNED_SPLIT_EVIDENCE_OUTPUT_NAMES
    ]


def _request_entry_digest_payload(entry: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(entry)
    payload.pop("per_ticker_split_provider_evidence_request_approval_digest", None)
    return payload


def per_ticker_split_provider_evidence_request_approval_digest_v1(
    entry: dict[str, Any],
) -> str:
    """Return the deterministic digest for one per-ticker request approval entry."""
    return semantic_digest(_request_entry_digest_payload(entry))


def _request_entries(source_review: dict[str, Any]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for source in source_review["per_ticker_split_event_review_entries"]:
        entry = {
            "ticker": source["ticker"],
            "split_event_candidate_status": source["split_event_candidate_status"],
            "split_event_review_status": source["split_event_review_status"],
            "split_provider_evidence_request_status": AUTHORIZED_NOT_EXECUTED,
            "split_provider_evidence_execution_status": NOT_EXECUTED,
            "split_provider_evidence_results_status": NOT_CREATED,
            "split_event_authority_status": source["split_event_authority_status"],
            "split_event_freeze_status": source["split_event_freeze_status"],
            "dividend_event_authority_status": NOT_CREATED,
            "corporate_action_authority_created": False,
            "acquisition_authorized": False,
            "dataset_generation_authorized": False,
            "runtime_use": _not_authorized(),
            "strategy_use": _not_authorized(),
            "paper_trading": _not_authorized(),
            "broker_execution": _not_authorized(),
            "source_split_event_candidate_digest": (
                EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_DIGEST
            ),
            "source_split_event_review_digest": source[
                "per_ticker_split_event_review_digest"
            ],
            "source_corporate_action_plan_approval_digest": source[
                "source_corporate_action_plan_approval_digest"
            ],
        }
        entry["per_ticker_split_provider_evidence_request_approval_digest"] = (
            per_ticker_split_provider_evidence_request_approval_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _attestation_checks(attestation: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not isinstance(attestation, dict):
        return [
            _check(
                "operator_decision_approved",
                OPERATOR_DECISION_APPROVE_SPLIT_PROVIDER_EVIDENCE_REQUEST,
                None,
            ),
            _check(
                "operator_attestation_phrase_matches",
                REQUIRED_SPLIT_PROVIDER_EVIDENCE_REQUEST_APPROVAL_ATTESTATION_PHRASE,
                None,
            ),
            _check(
                "operator_split_candidate_review_digest_confirmation_matches",
                EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
                None,
            ),
            _check(
                "operator_split_candidate_digest_confirmation_matches",
                EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_DIGEST,
                None,
            ),
            _check(
                "operator_dividend_candidate_review_digest_confirmation_matches",
                EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
                None,
            ),
            _check(
                "operator_corporate_action_plan_approval_digest_confirmation_matches",
                EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST,
                None,
            ),
            _check(
                "operator_registry_inventory_approval_digest_confirmation_matches",
                EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST,
                None,
            ),
            _check(
                "operator_identity_freeze_digest_confirmation_matches",
                EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
                None,
            ),
            _check("operator_target_universe_confirmation_matches", VALIDATION_TARGET_UNIVERSE, None),
            _check("operator_target_count_confirmation_matches", 12, None),
            *[_check(field, True, None) for field in OPERATOR_CONFIRMATION_FIELDS],
        ]
    return [
        _check(
            "operator_decision_approved",
            OPERATOR_DECISION_APPROVE_SPLIT_PROVIDER_EVIDENCE_REQUEST,
            attestation.get("operator_decision"),
        ),
        _check(
            "operator_attestation_phrase_matches",
            REQUIRED_SPLIT_PROVIDER_EVIDENCE_REQUEST_APPROVAL_ATTESTATION_PHRASE,
            attestation.get("operator_attestation_phrase"),
        ),
        _check(
            "operator_split_candidate_review_digest_confirmation_matches",
            EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
            attestation.get("operator_confirms_split_candidate_review_package_digest"),
        ),
        _check(
            "operator_split_candidate_digest_confirmation_matches",
            EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_DIGEST,
            attestation.get("operator_confirms_split_candidate_digest"),
        ),
        _check(
            "operator_dividend_candidate_review_digest_confirmation_matches",
            EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
            attestation.get("operator_confirms_dividend_candidate_review_package_digest"),
        ),
        _check(
            "operator_corporate_action_plan_approval_digest_confirmation_matches",
            EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST,
            attestation.get("operator_confirms_corporate_action_plan_approval_digest"),
        ),
        _check(
            "operator_registry_inventory_approval_digest_confirmation_matches",
            EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST,
            attestation.get("operator_confirms_registry_inventory_approval_digest"),
        ),
        _check(
            "operator_identity_freeze_digest_confirmation_matches",
            EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
            attestation.get("operator_confirms_identity_freeze_digest"),
        ),
        _check(
            "operator_target_universe_confirmation_matches",
            VALIDATION_TARGET_UNIVERSE,
            attestation.get("operator_confirms_target_universe"),
        ),
        _check(
            "operator_target_count_confirmation_matches",
            12,
            attestation.get("operator_confirms_target_count"),
        ),
        *[_check(field, True, attestation.get(field)) for field in OPERATOR_CONFIRMATION_FIELDS],
    ]


def _validated_operator_attestation(attestation: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(attestation, dict):
        raise SplitProviderEvidenceRequestApprovalError(
            "operator_attestation must be a JSON object"
        )
    for field in (
        "operator_reference",
        "operator_attestation_timestamp_utc",
        "operator_attestation_version",
    ):
        value = attestation.get(field)
        if not isinstance(value, str) or not value.strip():
            raise SplitProviderEvidenceRequestApprovalError(
                f"{field} must be a non-empty string"
            )
    failed = [item for item in _attestation_checks(attestation) if item["status"] != PASS]
    if failed:
        raise SplitProviderEvidenceRequestApprovalError(
            f"operator attestation failed: {failed[0]['check_id']}"
        )
    return deepcopy(attestation)


def _digests_present(entries: list[dict[str, Any]], field_name: str) -> bool:
    return all(
        isinstance(entry.get(field_name), str) and len(entry[field_name]) == 64
        for entry in entries
    )


def _all_entry_field(entries: list[dict[str, Any]], field_name: str, expected: Any) -> bool:
    return len(entries) == 12 and all(entry.get(field_name) == expected for entry in entries)


def _planned_outputs_not_generated(approved: dict[str, Any]) -> bool:
    outputs = approved.get("planned_outputs")
    return isinstance(outputs, list) and bool(outputs) and all(
        item.get("generation_status") == PLANNED_NOT_GENERATED
        and item.get("generated") is False
        for item in outputs
    )


def _planned_outputs_research_only(approved: dict[str, Any]) -> bool:
    outputs = approved.get("planned_outputs")
    return isinstance(outputs, list) and bool(outputs) and all(
        item.get("actionability") == RESEARCH_ONLY_NON_ACTIONABLE
        for item in outputs
    )


def _approval_checklist(approved: dict[str, Any]) -> list[dict[str, Any]]:
    entries = approved.get("per_ticker_split_provider_evidence_request_approval_entries")
    entries = entries if isinstance(entries, list) else []
    return [
        _check("split_candidate_review_digest_matches_expected", EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST, approved.get("split_event_authority_candidate_review_package_digest")),
        _check("split_candidate_review_has_zero_blockers", 0, approved.get("source_split_event_authority_candidate_review_blocker_count")),
        _check("split_candidate_digest_matches_expected", EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_DIGEST, approved.get("split_event_authority_candidate_digest")),
        _check("dividend_candidate_review_digest_matches_expected", EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST, approved.get("dividend_event_authority_candidate_review_package_digest")),
        _check("dividend_candidate_digest_matches_expected", EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_DIGEST, approved.get("dividend_event_authority_candidate_digest")),
        _check("corporate_action_plan_approval_digest_bound", EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST, approved.get("corporate_action_authority_plan_approval_digest")),
        _check("corporate_action_plan_review_digest_bound", EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST, approved.get("corporate_action_authority_plan_candidate_review_package_digest")),
        _check("corporate_action_plan_candidate_digest_bound", EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_DIGEST, approved.get("corporate_action_authority_plan_candidate_digest")),
        _check("registry_inventory_approval_digest_bound", EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST, approved.get("post_identity_freeze_registry_inventory_approval_digest")),
        _check("identity_freeze_digest_bound", EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST, approved.get("identity_authority_freeze_digest")),
        _check("live_validation_results_review_digest_bound", EXPECTED_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_DIGEST, approved.get("live_ticker_validation_results_review_package_digest")),
        _check("ticker_universe_selection_approval_digest_bound", EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST, approved.get("ticker_universe_selection_approval_digest")),
        _check("target_universe_count_12", 12, approved.get("target_universe_count")),
        _check("target_universe_matches_expected", VALIDATION_TARGET_UNIVERSE, approved.get("target_universe")),
        _check("approval_scope_read_only_split_evidence_request_only", READ_ONLY_SPLIT_EVENT_EVIDENCE_REQUEST_APPROVAL_ONLY, approved.get("approval_scope")),
        _check("split_provider_evidence_request_objective_matches", SPLIT_PROVIDER_EVIDENCE_REQUEST_OBJECTIVE, approved.get("split_provider_evidence_request_objective")),
        _check("split_provider_evidence_request_scope_matches", SPLIT_PROVIDER_EVIDENCE_REQUEST_SCOPE, approved.get("split_provider_evidence_request_scope")),
        _check("split_provider_evidence_authority_scope_evidence_only", SPLIT_PROVIDER_EVIDENCE_AUTHORITY_SCOPE, approved.get("split_provider_evidence_authority_scope")),
        _check("split_provider_evidence_execution_status_not_executed", NOT_EXECUTED, approved.get("split_provider_evidence_execution_status")),
        _check("read_only_request_policy_matches", READ_ONLY_REQUEST_POLICY, approved.get("read_only_request_policy")),
        _check("per_ticker_split_provider_request_entries_12", 12, len(entries)),
        _check("per_ticker_split_candidate_status_ready", True, _all_entry_field(entries, "split_event_candidate_status", split_review.candidate_service.SPLIT_EVENT_CANDIDATE_READY_FOR_OPERATOR_REVIEW)),
        _check("per_ticker_split_review_status_ready", True, _all_entry_field(entries, "split_event_review_status", split_review.READY_FOR_OPERATOR_ASSESSMENT)),
        _check("per_ticker_request_status_authorized_not_executed", True, _all_entry_field(entries, "split_provider_evidence_request_status", AUTHORIZED_NOT_EXECUTED)),
        _check("per_ticker_execution_status_not_executed", True, _all_entry_field(entries, "split_provider_evidence_execution_status", NOT_EXECUTED)),
        _check("per_ticker_results_status_not_created", True, _all_entry_field(entries, "split_provider_evidence_results_status", NOT_CREATED)),
        _check("per_ticker_split_authority_not_created", True, _all_entry_field(entries, "split_event_authority_status", split_review.candidate_service.NOT_CREATED)),
        _check("per_ticker_split_freeze_not_frozen", True, _all_entry_field(entries, "split_event_freeze_status", split_review.candidate_service.NOT_FROZEN)),
        _check("per_ticker_dividend_authority_not_created", True, _all_entry_field(entries, "dividend_event_authority_status", NOT_CREATED)),
        _check("per_ticker_corporate_action_authority_false", True, _all_entry_field(entries, "corporate_action_authority_created", False)),
        _check("per_ticker_acquisition_authorized_false", True, _all_entry_field(entries, "acquisition_authorized", False)),
        _check("per_ticker_dataset_generation_authorized_false", True, _all_entry_field(entries, "dataset_generation_authorized", False)),
        _check("per_ticker_runtime_use_not_authorized", True, _all_entry_field(entries, "runtime_use", _not_authorized())),
        _check("per_ticker_strategy_use_not_authorized", True, _all_entry_field(entries, "strategy_use", _not_authorized())),
        _check("per_ticker_paper_trading_not_authorized", True, _all_entry_field(entries, "paper_trading", _not_authorized())),
        _check("per_ticker_broker_execution_not_authorized", True, _all_entry_field(entries, "broker_execution", _not_authorized())),
        _check("per_ticker_source_split_candidate_digests_present", True, _digests_present(entries, "source_split_event_candidate_digest")),
        _check("per_ticker_source_split_review_digests_present", True, _digests_present(entries, "source_split_event_review_digest")),
        _check("per_ticker_source_plan_approval_digests_present", True, _digests_present(entries, "source_corporate_action_plan_approval_digest")),
        _check("per_ticker_request_approval_digests_present", True, _digests_present(entries, "per_ticker_split_provider_evidence_request_approval_digest")),
        *_attestation_checks(approved.get("operator_attestation") if isinstance(approved.get("operator_attestation"), dict) else None),
        _check("split_provider_evidence_request_authorized_true", True, approved.get("split_provider_evidence_request_authorized")),
        _check("ready_for_split_provider_evidence_execution_true", True, approved.get("ready_for_split_provider_evidence_execution")),
        _check("provider_requests_made_in_approval_false", False, approved.get("provider_requests_made_in_approval")),
        _check("live_provider_transport_enabled_in_approval_false", False, approved.get("live_provider_transport_enabled_in_approval")),
        _check("split_provider_evidence_executed_false", False, approved.get("split_provider_evidence_executed")),
        _check("split_provider_evidence_results_created_false", False, approved.get("split_provider_evidence_results_created")),
        _check("split_event_authority_created_false", False, approved.get("split_event_authority_created")),
        _check("split_event_authority_frozen_false", False, approved.get("split_event_authority_frozen")),
        _check("dividend_provider_evidence_request_authorized_false", False, approved.get("dividend_provider_evidence_request_authorized")),
        _check("dividend_provider_evidence_executed_false", False, approved.get("dividend_provider_evidence_executed")),
        _check("dividend_provider_evidence_results_created_false", False, approved.get("dividend_provider_evidence_results_created")),
        _check("dividend_event_authority_created_false", False, approved.get("dividend_event_authority_created")),
        _check("dividend_event_authority_frozen_false", False, approved.get("dividend_event_authority_frozen")),
        _check("corporate_action_authority_created_false", False, approved.get("corporate_action_authority_created")),
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
        _check("profitability_not_accepted", acquisition.PROFITABILITY_NOT_ACCEPTED, approved.get("profitability"), severity=INFO),
        _check("runtime_migration_approved_false", False, approved.get("runtime_migration_approved")),
        _check("runtime_use_not_authorized", _not_authorized(), approved.get("runtime_use")),
        _check("strategy_use_not_authorized", _not_authorized(), approved.get("strategy_use")),
        _check("paper_trading_not_authorized", _not_authorized(), approved.get("paper_trading")),
        _check("broker_execution_not_authorized", _not_authorized(), approved.get("broker_execution")),
        _check("automatic_stitching_false", False, approved.get("automatic_stitching")),
        _check("planned_outputs_not_generated", True, _planned_outputs_not_generated(approved)),
        _check("planned_outputs_research_only", True, _planned_outputs_research_only(approved)),
        _check("no_split_provider_evidence_execution_created", False, approved.get("split_provider_evidence_execution_created")),
        _check("no_split_event_authority_artifact_created", False, approved.get("split_event_authority_artifact_created")),
        _check("no_split_event_authority_freeze_created", False, approved.get("split_event_authority_freeze_created")),
        _check("no_dividend_event_authority_artifact_created", False, approved.get("dividend_event_authority_artifact_created")),
        _check("no_corporate_action_authority_artifact_created", False, approved.get("corporate_action_authority_artifact_created")),
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
        "split_provider_evidence_request_authorized_by_operator": not failed,
        "ready_for_split_provider_evidence_execution": not failed,
        "split_provider_evidence_executed": False,
        "split_event_authority_authorized": False,
        "split_event_authority_frozen": False,
        "dividend_provider_evidence_request_authorized": False,
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


def _digest_payload(approved_artifact: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(approved_artifact)
    payload.pop("split_provider_evidence_request_approval_digest", None)
    return payload


def split_provider_evidence_request_approval_digest_v1(
    approved_artifact: dict[str, Any],
) -> str:
    """Return the deterministic digest for the split provider request approval."""
    return semantic_digest(_digest_payload(approved_artifact))


def build_split_provider_evidence_request_approved_v1(
    *,
    split_candidate_review_package: dict[str, Any] | None = None,
    dividend_candidate_review_package: dict[str, Any] | None = None,
    operator_attestation: dict[str, Any],
) -> dict[str, Any]:
    """Build an offline approval artifact for future read-only split evidence requests."""
    split_source = _source_split_review_package(split_candidate_review_package)
    dividend_source = _source_dividend_review_package(dividend_candidate_review_package)
    attestation = _validated_operator_attestation(operator_attestation)
    approved: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND_SPLIT_PROVIDER_EVIDENCE_REQUEST_APPROVED,
        "schema_version": SCHEMA_VERSION_SPLIT_PROVIDER_EVIDENCE_REQUEST_APPROVAL_V1,
        "approval_status": SPLIT_PROVIDER_EVIDENCE_REQUEST_APPROVED,
        "approval_scope": READ_ONLY_SPLIT_EVENT_EVIDENCE_REQUEST_APPROVAL_ONLY,
        "created_offline": True,
        "provider_requests_made_in_approval": False,
        "live_provider_transport_enabled_in_approval": False,
        "split_event_authority_candidate_created": True,
        "split_event_authority_review_created": True,
        "split_event_authority_created": False,
        "split_event_authority_frozen": False,
        "split_event_authority_artifact_created": False,
        "split_event_authority_freeze_created": False,
        "split_provider_evidence_request_authorized": True,
        "ready_for_split_provider_evidence_execution": True,
        "split_provider_evidence_executed": False,
        "split_provider_evidence_results_created": False,
        "split_provider_evidence_execution_created": False,
        "dividend_event_authority_candidate_created": True,
        "dividend_event_authority_review_created": True,
        "dividend_event_authority_created": False,
        "dividend_event_authority_frozen": False,
        "dividend_event_authority_artifact_created": False,
        "dividend_provider_evidence_request_authorized": False,
        "dividend_provider_evidence_executed": False,
        "dividend_provider_evidence_results_created": False,
        "corporate_action_authority_plan_approved": True,
        "corporate_action_authority_created": False,
        "corporate_action_authority_artifact_created": False,
        "post_identity_freeze_registry_inventory_approved": True,
        "identity_authority_created": True,
        "identity_authority_frozen": True,
        "new_ticker_identity_authority_created": True,
        "authority_scope": (
            split_review.candidate_service.approval.review.plan.approval_service.review_service.candidate_service.freeze_service.IDENTITY_AUTHORITY_ONLY
        ),
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
        "split_event_authority_candidate_review_package_digest": split_source[
            "split_event_authority_candidate_review_package_digest"
        ],
        "source_split_event_authority_candidate_review_blocker_count": split_source[
            "review_summary"
        ]["blocker_count"],
        "split_event_authority_candidate_digest": split_source[
            "split_event_authority_candidate_digest"
        ],
        "dividend_event_authority_candidate_review_package_digest": dividend_source[
            "dividend_event_authority_candidate_review_package_digest"
        ],
        "dividend_event_authority_candidate_digest": dividend_source[
            "dividend_event_authority_candidate_digest"
        ],
        "corporate_action_authority_plan_approval_digest": split_source[
            "corporate_action_authority_plan_approval_digest"
        ],
        "corporate_action_authority_plan_candidate_review_package_digest": split_source[
            "corporate_action_authority_plan_candidate_review_package_digest"
        ],
        "corporate_action_authority_plan_candidate_digest": split_source[
            "corporate_action_authority_plan_candidate_digest"
        ],
        "post_identity_freeze_registry_inventory_approval_digest": split_source[
            "post_identity_freeze_registry_inventory_approval_digest"
        ],
        "identity_authority_freeze_digest": split_source["identity_authority_freeze_digest"],
        "live_ticker_validation_results_review_package_digest": split_source[
            "live_ticker_validation_results_review_package_digest"
        ],
        "ticker_universe_selection_approval_digest": split_source[
            "ticker_universe_selection_approval_digest"
        ],
        "target_universe": list(split_source["target_universe"]),
        "target_universe_count": split_source["target_universe_count"],
        "split_provider_evidence_request_objective": SPLIT_PROVIDER_EVIDENCE_REQUEST_OBJECTIVE,
        "split_provider_evidence_request_scope": SPLIT_PROVIDER_EVIDENCE_REQUEST_SCOPE,
        "split_provider_evidence_authority_scope": SPLIT_PROVIDER_EVIDENCE_AUTHORITY_SCOPE,
        "split_provider_evidence_execution_status": NOT_EXECUTED,
        "read_only_request_policy": deepcopy(READ_ONLY_REQUEST_POLICY),
        "planned_outputs": _planned_outputs(),
        "planned_output_count": len(PLANNED_SPLIT_EVIDENCE_OUTPUT_NAMES),
        "planned_outputs_status": PLANNED_NOT_GENERATED,
        "planned_outputs_label": RESEARCH_ONLY_NON_ACTIONABLE,
        "operator_attestation": attestation,
        "remaining_roadmap": list(REMAINING_ROADMAP_AFTER_APPROVAL),
    }
    approved["per_ticker_split_provider_evidence_request_approval_entries"] = (
        _request_entries(split_source)
    )
    checklist = _approval_checklist(approved)
    approved["approval_checklist"] = checklist
    approved["approval_summary"] = _summary(checklist)
    approved["split_provider_evidence_request_approval_digest"] = (
        split_provider_evidence_request_approval_digest_v1(approved)
    )
    validate_split_provider_evidence_request_approved_v1(approved)
    return approved


def _reject_forbidden_values(
    mapping: dict[str, Any], *, path: str = "approved_artifact"
) -> None:
    forbidden_strings = {
        "SPLIT_EVENT_PROVIDER_EVIDENCE_EXECUTED",
        "SPLIT_EVENT_PROVIDER_EVIDENCE_RESULTS",
        "SPLIT_EVENT_AUTHORITY_APPROVED",
        "SPLIT_EVENT_AUTHORITY_FROZEN",
        "DIVIDEND_EVENT_PROVIDER_EVIDENCE_REQUEST_APPROVED",
        "DIVIDEND_EVENT_PROVIDER_EVIDENCE_EXECUTED",
        "DIVIDEND_EVENT_AUTHORITY_APPROVED",
        "DIVIDEND_EVENT_AUTHORITY_FROZEN",
        "CORPORATE_ACTION_AUTHORITY_APPROVED",
        "NEW_TICKER_ACQUISITION_AUTHORIZED",
        "ACQUISITION_GENERATION_AUTHORIZED",
        "CANONICAL_DATASET_AUTHORIZED",
        "REGISTRY_APPROVAL_CREATED",
        "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED",
        "PREDICTIVE_USEFULNESS_ACCEPTANCE_CANDIDATE",
        "PREDICTIVE_USEFULNESS_ACCEPTED",
        "PROFITABILITY_ACCEPTED",
        "RUNTIME_MIGRATION_APPROVED",
        "RUNTIME_MIGRATION_ACTIVE",
        "STRATEGY_RUNTIME_MIGRATION",
        "TRADE_RECOMMENDATIONS",
    }
    forbidden_true_fields = {
        "provider_requests_made",
        "provider_requests_made_in_approval",
        "live_provider_transport_enabled",
        "live_provider_transport_enabled_in_approval",
        "split_provider_evidence_executed",
        "split_provider_evidence_results_created",
        "split_provider_evidence_execution_created",
        "split_event_authority_created",
        "split_event_authority_frozen",
        "split_event_authority_artifact_created",
        "split_event_authority_freeze_created",
        "dividend_provider_evidence_request_authorized",
        "dividend_provider_evidence_executed",
        "dividend_provider_evidence_results_created",
        "dividend_event_authority_created",
        "dividend_event_authority_frozen",
        "dividend_event_authority_artifact_created",
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
    }
    for key, value in mapping.items():
        current_path = f"{path}.{key}"
        if isinstance(value, str) and value in forbidden_strings:
            raise SplitProviderEvidenceRequestApprovalError(
                f"{current_path} must not emit {value}"
            )
        if key in forbidden_true_fields and value is True:
            raise SplitProviderEvidenceRequestApprovalError(
                f"{current_path} must be false"
            )
        if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and value == "AUTHORIZED":
            raise SplitProviderEvidenceRequestApprovalError(
                f"{current_path} must not be AUTHORIZED"
            )
        if key in {"predictive_usefulness", "profitability"} and value == "accepted":
            raise SplitProviderEvidenceRequestApprovalError(
                f"{current_path} must not be accepted"
            )
        if isinstance(value, dict):
            _reject_forbidden_values(value, path=current_path)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, dict):
                    _reject_forbidden_values(item, path=f"{current_path}[{index}]")


def _validate_request_entries(approved_artifact: dict[str, Any]) -> None:
    entries = approved_artifact.get(
        "per_ticker_split_provider_evidence_request_approval_entries"
    )
    if not isinstance(entries, list) or len(entries) != 12:
        raise SplitProviderEvidenceRequestApprovalError(
            "per_ticker_split_provider_evidence_request_approval_entries mismatch"
        )
    _expect(
        [entry.get("ticker") for entry in entries],
        VALIDATION_TARGET_UNIVERSE,
        "per_ticker_split_provider_evidence_request_approval_entries tickers",
    )
    for entry in entries:
        ticker = entry.get("ticker")
        for field, expected in {
            "split_event_candidate_status": split_review.candidate_service.SPLIT_EVENT_CANDIDATE_READY_FOR_OPERATOR_REVIEW,
            "split_event_review_status": split_review.READY_FOR_OPERATOR_ASSESSMENT,
            "split_provider_evidence_request_status": AUTHORIZED_NOT_EXECUTED,
            "split_provider_evidence_execution_status": NOT_EXECUTED,
            "split_provider_evidence_results_status": NOT_CREATED,
            "split_event_authority_status": split_review.candidate_service.NOT_CREATED,
            "split_event_freeze_status": split_review.candidate_service.NOT_FROZEN,
            "dividend_event_authority_status": NOT_CREATED,
            "runtime_use": _not_authorized(),
            "strategy_use": _not_authorized(),
            "paper_trading": _not_authorized(),
            "broker_execution": _not_authorized(),
        }.items():
            _expect(entry.get(field), expected, f"{ticker}.{field}")
        for field in (
            "corporate_action_authority_created",
            "acquisition_authorized",
            "dataset_generation_authorized",
        ):
            _expect_false(entry.get(field), f"{ticker}.{field}")
        for field in (
            "source_split_event_candidate_digest",
            "source_split_event_review_digest",
            "source_corporate_action_plan_approval_digest",
            "per_ticker_split_provider_evidence_request_approval_digest",
        ):
            digest = entry.get(field)
            if not isinstance(digest, str) or len(digest) != 64:
                raise SplitProviderEvidenceRequestApprovalError(f"{field} missing")
        _expect(
            entry["source_split_event_candidate_digest"],
            approved_artifact["split_event_authority_candidate_digest"],
            f"{ticker}.source_split_event_candidate_digest",
        )
        _expect(
            entry["source_corporate_action_plan_approval_digest"],
            approved_artifact["corporate_action_authority_plan_approval_digest"],
            f"{ticker}.source_corporate_action_plan_approval_digest",
        )
        _expect(
            entry["per_ticker_split_provider_evidence_request_approval_digest"],
            per_ticker_split_provider_evidence_request_approval_digest_v1(entry),
            f"{ticker}.per_ticker_split_provider_evidence_request_approval_digest",
        )


def validate_split_provider_evidence_request_approved_v1(
    approved_artifact: dict[str, Any],
) -> dict[str, Any]:
    """Validate the split provider evidence request approval artifact."""
    if not isinstance(approved_artifact, dict):
        raise SplitProviderEvidenceRequestApprovalError(
            "approved artifact must be a JSON object"
        )
    _reject_forbidden_values(approved_artifact)
    _expect(
        approved_artifact.get("artifact_kind"),
        ARTIFACT_KIND_SPLIT_PROVIDER_EVIDENCE_REQUEST_APPROVED,
        "artifact_kind",
    )
    _expect(
        approved_artifact.get("schema_version"),
        SCHEMA_VERSION_SPLIT_PROVIDER_EVIDENCE_REQUEST_APPROVAL_V1,
        "schema_version",
    )
    _expect(
        approved_artifact.get("approval_status"),
        SPLIT_PROVIDER_EVIDENCE_REQUEST_APPROVED,
        "approval_status",
    )
    for field in (
        "created_offline",
        "split_event_authority_candidate_created",
        "split_event_authority_review_created",
        "split_provider_evidence_request_authorized",
        "ready_for_split_provider_evidence_execution",
        "dividend_event_authority_candidate_created",
        "dividend_event_authority_review_created",
        "corporate_action_authority_plan_approved",
        "post_identity_freeze_registry_inventory_approved",
        "identity_authority_created",
        "identity_authority_frozen",
        "new_ticker_identity_authority_created",
        "research_only",
    ):
        _expect_true(approved_artifact.get(field), field)
    for field in (
        "provider_requests_made_in_approval",
        "live_provider_transport_enabled_in_approval",
        "split_provider_evidence_executed",
        "split_provider_evidence_results_created",
        "split_provider_evidence_execution_created",
        "split_event_authority_created",
        "split_event_authority_frozen",
        "split_event_authority_artifact_created",
        "split_event_authority_freeze_created",
        "dividend_provider_evidence_request_authorized",
        "dividend_provider_evidence_executed",
        "dividend_provider_evidence_results_created",
        "dividend_event_authority_created",
        "dividend_event_authority_frozen",
        "dividend_event_authority_artifact_created",
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
    ):
        _expect_false(approved_artifact.get(field), field)
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(approved_artifact.get(field), _not_authorized(), field)
    for field, expected in {
        "approval_scope": READ_ONLY_SPLIT_EVENT_EVIDENCE_REQUEST_APPROVAL_ONLY,
        "split_event_authority_candidate_review_package_digest": EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "source_split_event_authority_candidate_review_blocker_count": 0,
        "split_event_authority_candidate_digest": EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_DIGEST,
        "dividend_event_authority_candidate_review_package_digest": EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "dividend_event_authority_candidate_digest": EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_DIGEST,
        "corporate_action_authority_plan_approval_digest": EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST,
        "corporate_action_authority_plan_candidate_review_package_digest": EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "corporate_action_authority_plan_candidate_digest": EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_DIGEST,
        "post_identity_freeze_registry_inventory_approval_digest": EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST,
        "identity_authority_freeze_digest": EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
        "live_ticker_validation_results_review_package_digest": EXPECTED_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_DIGEST,
        "ticker_universe_selection_approval_digest": EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST,
        "target_universe": VALIDATION_TARGET_UNIVERSE,
        "target_universe_count": 12,
        "authority_scope": split_review.candidate_service.approval.review.plan.approval_service.review_service.candidate_service.freeze_service.IDENTITY_AUTHORITY_ONLY,
        "split_provider_evidence_request_objective": SPLIT_PROVIDER_EVIDENCE_REQUEST_OBJECTIVE,
        "split_provider_evidence_request_scope": SPLIT_PROVIDER_EVIDENCE_REQUEST_SCOPE,
        "split_provider_evidence_authority_scope": SPLIT_PROVIDER_EVIDENCE_AUTHORITY_SCOPE,
        "split_provider_evidence_execution_status": NOT_EXECUTED,
        "read_only_request_policy": READ_ONLY_REQUEST_POLICY,
        "planned_output_count": 6,
        "planned_outputs_status": PLANNED_NOT_GENERATED,
        "planned_outputs_label": RESEARCH_ONLY_NON_ACTIONABLE,
        "remaining_roadmap": REMAINING_ROADMAP_AFTER_APPROVAL,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
    }.items():
        _expect(approved_artifact.get(field), expected, field)
    if not _planned_outputs_not_generated(approved_artifact):
        raise SplitProviderEvidenceRequestApprovalError(
            "planned_outputs must not be generated"
        )
    if not _planned_outputs_research_only(approved_artifact):
        raise SplitProviderEvidenceRequestApprovalError(
            "planned_outputs must be research only"
        )
    _validate_request_entries(approved_artifact)
    _validated_operator_attestation(approved_artifact.get("operator_attestation"))
    checklist = _approval_checklist(approved_artifact)
    _expect(
        [item["check_id"] for item in checklist],
        REQUIRED_APPROVAL_CHECK_IDS,
        "approval_checklist check IDs",
    )
    failed = [item for item in checklist if item["status"] != PASS]
    if failed:
        raise SplitProviderEvidenceRequestApprovalError(
            f"approval checklist contains failed check: {failed[0]['check_id']}"
        )
    _expect(approved_artifact.get("approval_checklist"), checklist, "approval_checklist")
    summary = _summary(checklist)
    _expect(approved_artifact.get("approval_summary"), summary, "approval_summary")
    _expect_true(
        summary.get("split_provider_evidence_request_authorized_by_operator"),
        "split_provider_evidence_request_authorized_by_operator",
    )
    _expect_true(
        summary.get("ready_for_split_provider_evidence_execution"),
        "ready_for_split_provider_evidence_execution",
    )
    for field in (
        "split_provider_evidence_executed",
        "split_event_authority_authorized",
        "split_event_authority_frozen",
        "dividend_provider_evidence_request_authorized",
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
    digest = approved_artifact.get("split_provider_evidence_request_approval_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise SplitProviderEvidenceRequestApprovalError(
            "split_provider_evidence_request_approval_digest missing"
        )
    _expect(
        digest,
        split_provider_evidence_request_approval_digest_v1(approved_artifact),
        "split_provider_evidence_request_approval_digest",
    )
    return {
        "status": "SPLIT_PROVIDER_EVIDENCE_REQUEST_APPROVED_VALID",
        "artifact_kind": approved_artifact["artifact_kind"],
        "approval_status": approved_artifact["approval_status"],
        "approval_scope": approved_artifact["approval_scope"],
        "split_provider_evidence_request_approval_digest": digest,
        "split_event_authority_candidate_review_package_digest": approved_artifact[
            "split_event_authority_candidate_review_package_digest"
        ],
        "split_event_authority_candidate_digest": approved_artifact[
            "split_event_authority_candidate_digest"
        ],
        "dividend_event_authority_candidate_review_package_digest": approved_artifact[
            "dividend_event_authority_candidate_review_package_digest"
        ],
        "corporate_action_authority_plan_approval_digest": approved_artifact[
            "corporate_action_authority_plan_approval_digest"
        ],
        "post_identity_freeze_registry_inventory_approval_digest": approved_artifact[
            "post_identity_freeze_registry_inventory_approval_digest"
        ],
        "identity_authority_freeze_digest": approved_artifact[
            "identity_authority_freeze_digest"
        ],
        "target_universe_count": approved_artifact["target_universe_count"],
        "per_ticker_split_provider_evidence_request_approval_entry_count": len(
            approved_artifact[
                "per_ticker_split_provider_evidence_request_approval_entries"
            ]
        ),
        "total_checks": summary["total_checks"],
        "passed_checks": summary["passed_checks"],
        "failed_checks": summary["failed_checks"],
        "blocker_count": summary["blocker_count"],
        "split_provider_evidence_request_authorized_by_operator": True,
        "ready_for_split_provider_evidence_execution": True,
        "split_provider_evidence_executed": False,
        "split_event_authority_authorized": False,
        "split_event_authority_frozen": False,
        "dividend_provider_evidence_request_authorized": False,
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


def build_split_provider_evidence_request_approved_markdown_v1(
    approved_artifact: dict[str, Any],
) -> str:
    """Render a sanitized split provider evidence request approval status document."""
    validation = validate_split_provider_evidence_request_approved_v1(
        approved_artifact
    )
    summary = approved_artifact["approval_summary"]
    lines = [
        "# MarketFlow Split Provider Evidence Request Approval Status",
        "",
        "## Title",
        "- Split Provider Evidence Request Approval Ceremony v1.",
        "",
        "## Approved Split Provider Evidence Request",
        f"- Artifact kind: `{approved_artifact['artifact_kind']}`",
        f"- Approval status: `{approved_artifact['approval_status']}`",
        f"- Approval scope: `{approved_artifact['approval_scope']}`",
        f"- Approval digest: `{validation['split_provider_evidence_request_approval_digest']}`",
        "",
        "## Operator Attestation",
        f"- Operator decision: `{approved_artifact['operator_attestation']['operator_decision']}`",
        f"- Operator reference: `{approved_artifact['operator_attestation']['operator_reference']}`",
        f"- Operator attestation version: `{approved_artifact['operator_attestation']['operator_attestation_version']}`",
        "",
        "## Source Split Candidate Review Package",
        f"- Split review package digest: `{approved_artifact['split_event_authority_candidate_review_package_digest']}`",
        f"- Split candidate digest: `{approved_artifact['split_event_authority_candidate_digest']}`",
        "",
        "## Source Dividend Candidate Review Package",
        f"- Dividend review package digest: `{approved_artifact['dividend_event_authority_candidate_review_package_digest']}`",
        f"- Dividend candidate digest: `{approved_artifact['dividend_event_authority_candidate_digest']}`",
        "",
        "## Target Universe",
        f"- Target universe count: `{approved_artifact['target_universe_count']}`",
        "- Target universe: "
        + ", ".join(f"`{ticker}`" for ticker in approved_artifact["target_universe"]),
        "",
        "## Approval Scope",
        f"- Objective: `{approved_artifact['split_provider_evidence_request_objective']}`",
        f"- Request scope: `{approved_artifact['split_provider_evidence_request_scope']}`",
        f"- Authority scope: `{approved_artifact['split_provider_evidence_authority_scope']}`",
        "",
        "## Read-Only Provider Request Boundary",
        f"- split_provider_evidence_request_authorized: `{approved_artifact['split_provider_evidence_request_authorized']}`",
        f"- ready_for_split_provider_evidence_execution: `{approved_artifact['ready_for_split_provider_evidence_execution']}`",
        f"- provider_requests_made_in_approval: `{approved_artifact['provider_requests_made_in_approval']}`",
        f"- live_provider_transport_enabled_in_approval: `{approved_artifact['live_provider_transport_enabled_in_approval']}`",
        "",
        "## Split Evidence Execution Boundary",
        f"- split_provider_evidence_executed: `{approved_artifact['split_provider_evidence_executed']}`",
        f"- split_provider_evidence_results_created: `{approved_artifact['split_provider_evidence_results_created']}`",
        "",
        "## Split Authority Boundary",
        f"- split_event_authority_created: `{approved_artifact['split_event_authority_created']}`",
        f"- split_event_authority_frozen: `{approved_artifact['split_event_authority_frozen']}`",
        "",
        "## Dividend Boundary",
        f"- dividend_provider_evidence_request_authorized: `{approved_artifact['dividend_provider_evidence_request_authorized']}`",
        f"- dividend_event_authority_created: `{approved_artifact['dividend_event_authority_created']}`",
        "",
        "## Corporate-Action Authority Boundary",
        f"- corporate_action_authority_created: `{approved_artifact['corporate_action_authority_created']}`",
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
        "",
        "## Remaining Required Tasks",
    ]
    lines.extend(f"{index}. {step}" for index, step in enumerate(approved_artifact["remaining_roadmap"], start=1))
    lines.extend(
        [
            "",
            "## Guardrails",
            "- No provider requests were made by this approval.",
            "- No live provider transport was enabled.",
            "- No split provider evidence execution or results were created.",
            "- No split, dividend, or corporate-action authority was created or frozen.",
            "- No acquisition, dataset, predictive, profitability, runtime, strategy, paper trading, broker execution, or trade recommendation path was authorized.",
            "",
        ]
    )
    return "\n".join(lines)


def write_split_provider_evidence_request_approved_v1(
    output_dir: str | Path,
    *,
    split_candidate_review_package: dict[str, Any] | None = None,
    dividend_candidate_review_package: dict[str, Any] | None = None,
    operator_attestation: dict[str, Any],
    filename: str | None = None,
) -> dict[str, Any]:
    """Write the approval artifact JSON without overwriting an existing file."""
    approved_artifact = build_split_provider_evidence_request_approved_v1(
        split_candidate_review_package=split_candidate_review_package,
        dividend_candidate_review_package=dividend_candidate_review_package,
        operator_attestation=operator_attestation,
    )
    validation = validate_split_provider_evidence_request_approved_v1(
        approved_artifact
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "split_provider_evidence_request_approved_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise SplitProviderEvidenceRequestApprovalError(
            "split provider evidence request approval filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise SplitProviderEvidenceRequestApprovalError(
            "split provider evidence request approval output already exists"
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
