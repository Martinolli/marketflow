"""Offline approval ceremony for future read-only live ticker validation."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import live_ticker_validation_candidate_operator_review_service as review


ARTIFACT_KIND_LIVE_TICKER_VALIDATION_APPROVED = "LIVE_TICKER_VALIDATION_APPROVED"
SCHEMA_VERSION_LIVE_TICKER_VALIDATION_APPROVAL_V1 = "live_ticker_validation_approval_v1"
LIVE_TICKER_VALIDATION_APPROVED = "LIVE_TICKER_VALIDATION_APPROVED"
READ_ONLY_PROVIDER_TICKER_VALIDATION_ONLY = "READ_ONLY_PROVIDER_TICKER_VALIDATION_ONLY"
OPERATOR_DECISION_APPROVE_LIVE_TICKER_VALIDATION = "APPROVE_LIVE_TICKER_VALIDATION"
OPERATOR_ATTESTATION_VERSION_V1 = "live_ticker_validation_approval_operator_attestation_v1"
REQUIRED_LIVE_TICKER_VALIDATION_APPROVAL_ATTESTATION_PHRASE = (
    "APPROVE LIVE TICKER VALIDATION MSFT NVDA AMZN GOOGL META TSLA JPM XOM JNJ WMT "
    "CAT LMT READ_ONLY_PROVIDER_VALIDATION_ONLY"
)

EXPECTED_LIVE_TICKER_VALIDATION_CANDIDATE_DIGEST = (
    review.EXPECTED_LIVE_TICKER_VALIDATION_CANDIDATE_DIGEST
)
EXPECTED_LIVE_TICKER_VALIDATION_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    "c38b723df9a66e94ff82696cf8c88aa5008e915e7fc42b2a8a760ea61623b3fc"
)
EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST = (
    review.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST
)
EXPECTED_REVIEW_CHECKLIST_FAILED = 0
EXPECTED_REVIEW_BLOCKER_COUNT = 0

APPROVED_EXPANDED_TICKER_UNIVERSE = list(review.APPROVED_EXPANDED_TICKER_UNIVERSE)
NOT_REQUESTED = review.NOT_REQUESTED
NOT_PERFORMED = review.NOT_PERFORMED
NOT_VERIFIED = review.NOT_VERIFIED
NOT_CREATED = review.NOT_CREATED
NOT_AUTHORIZED = review.NOT_AUTHORIZED
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

OPERATOR_CONFIRMATION_FIELDS = [
    "operator_confirms_approval_scope_read_only_provider_validation_only",
    "operator_confirms_provider_request_authorized",
    "operator_confirms_live_ticker_validation_authorized",
    "operator_confirms_no_provider_requests_made_in_approval",
    "operator_confirms_no_live_provider_transport_enabled",
    "operator_confirms_no_live_validation_performed",
    "operator_confirms_no_validation_results_created",
    "operator_confirms_no_new_ticker_authority",
    "operator_confirms_no_new_ticker_acquisition",
    "operator_confirms_no_dataset_generation_authorization",
    "operator_confirms_no_additional_predictive_evidence_execution_authorization",
    "operator_confirms_no_predictive_usefulness_acceptance",
    "operator_confirms_no_profitability_acceptance",
    "operator_confirms_no_runtime_migration_approval",
    "operator_confirms_no_runtime_activation",
    "operator_confirms_no_paper_trading",
    "operator_confirms_no_broker_execution",
    "operator_confirms_api_key_not_stored_or_printed",
    "operator_confirms_raw_payload_not_committed",
]

REMAINING_ROADMAP_AFTER_LIVE_TICKER_VALIDATION_APPROVAL = [
    "Live ticker validation execution.",
    "Live ticker validation results review.",
    "Per-ticker identity authority chain.",
    "Per-ticker corporate-action authority chain.",
    "Per-ticker acquisition authority chain.",
    "Dataset authority chain after validated ticker authority.",
]

REQUIRED_APPROVAL_CHECK_IDS = [
    "candidate_review_digest_matches_expected",
    "candidate_review_has_zero_blockers",
    "candidate_digest_matches_expected",
    "ticker_universe_selection_approval_digest_matches_expected",
    "validation_target_universe_matches_expected",
    "validation_target_count_12",
    "approval_scope_read_only_provider_validation_only",
    "operator_decision_approved",
    "operator_attestation_phrase_matches",
    "operator_confirms_candidate_digest",
    "operator_confirms_candidate_review_digest",
    "operator_confirms_ticker_universe_approval_digest",
    "operator_confirms_validation_target_universe",
    "operator_confirms_approval_scope_read_only_provider_validation_only",
    "operator_confirms_provider_request_authorized",
    "operator_confirms_live_ticker_validation_authorized",
    "operator_confirms_no_provider_requests_made_in_approval",
    "operator_confirms_no_live_provider_transport_enabled",
    "operator_confirms_no_live_validation_performed",
    "operator_confirms_no_validation_results_created",
    "operator_confirms_no_new_ticker_authority",
    "operator_confirms_no_new_ticker_acquisition",
    "operator_confirms_no_dataset_generation_authorization",
    "operator_confirms_no_additional_predictive_evidence_execution_authorization",
    "operator_confirms_no_predictive_usefulness_acceptance",
    "operator_confirms_no_profitability_acceptance",
    "operator_confirms_no_runtime_migration_approval",
    "operator_confirms_no_runtime_activation",
    "operator_confirms_no_paper_trading",
    "operator_confirms_no_broker_execution",
    "operator_confirms_api_key_not_stored_or_printed",
    "operator_confirms_raw_payload_not_committed",
    "provider_request_authorized_true",
    "live_ticker_validation_authorized_true",
    "provider_requests_made_false",
    "provider_requests_made_in_approval_false",
    "live_provider_transport_enabled_false",
    "live_ticker_validation_performed_false",
    "live_validation_results_created_false",
    "validation_targets_provider_request_not_requested",
    "validation_targets_live_validation_not_performed",
    "validation_targets_listing_not_verified",
    "validation_targets_authority_not_created",
    "validation_targets_runtime_not_authorized",
    "new_ticker_authority_created_false",
    "new_ticker_acquisition_authorized_false",
    "dataset_generation_authorized_false",
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
    "no_live_ticker_validation_execution_artifact_created",
    "no_live_validation_results_created",
    "no_new_ticker_authority_artifact_created",
    "no_acquisition_authorization_created",
    "no_dataset_generation_authorization_created",
    "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created",
    "no_runtime_migration_approval_created",
]


class LiveTickerValidationApprovalError(ValueError):
    """Raised when the live ticker validation approval violates guardrails."""


def _check(check_id: str, expected: Any, actual: Any, *, severity: str = BLOCKER) -> dict[str, Any]:
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
        raise LiveTickerValidationApprovalError(f"{field_name} mismatch")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise LiveTickerValidationApprovalError(f"{field_name} must be true")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise LiveTickerValidationApprovalError(f"{field_name} must be false")


def _path_text(path: Path) -> str:
    return str(path).replace("\\", "/")


def build_live_ticker_validation_approval_attestation_v1(
    *,
    operator_reference: str,
    operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str,
    operator_confirms_live_ticker_validation_candidate_digest: str,
    operator_confirms_live_ticker_validation_candidate_review_package_digest: str,
    operator_confirms_ticker_universe_selection_approval_digest: str,
    operator_confirms_validation_target_universe: list[str],
    operator_confirms_validation_target_count: int,
    operator_confirms_approval_scope_read_only_provider_validation_only: bool,
    operator_confirms_provider_request_authorized: bool,
    operator_confirms_live_ticker_validation_authorized: bool,
    operator_confirms_no_provider_requests_made_in_approval: bool,
    operator_confirms_no_live_provider_transport_enabled: bool,
    operator_confirms_no_live_validation_performed: bool,
    operator_confirms_no_validation_results_created: bool,
    operator_confirms_no_new_ticker_authority: bool,
    operator_confirms_no_new_ticker_acquisition: bool,
    operator_confirms_no_dataset_generation_authorization: bool,
    operator_confirms_no_additional_predictive_evidence_execution_authorization: bool,
    operator_confirms_no_predictive_usefulness_acceptance: bool,
    operator_confirms_no_profitability_acceptance: bool,
    operator_confirms_no_runtime_migration_approval: bool,
    operator_confirms_no_runtime_activation: bool,
    operator_confirms_no_paper_trading: bool,
    operator_confirms_no_broker_execution: bool,
    operator_confirms_api_key_not_stored_or_printed: bool,
    operator_confirms_raw_payload_not_committed: bool,
    operator_decision: str = OPERATOR_DECISION_APPROVE_LIVE_TICKER_VALIDATION,
    operator_attestation_version: str = OPERATOR_ATTESTATION_VERSION_V1,
) -> dict[str, Any]:
    """Build a non-secret operator attestation for read-only validation approval."""
    return {
        "operator_reference": operator_reference,
        "operator_decision": operator_decision,
        "operator_attestation_phrase": operator_attestation_phrase,
        "operator_attestation_timestamp_utc": operator_attestation_timestamp_utc,
        "operator_attestation_version": operator_attestation_version,
        "operator_confirms_live_ticker_validation_candidate_digest": (
            operator_confirms_live_ticker_validation_candidate_digest
        ),
        "operator_confirms_live_ticker_validation_candidate_review_package_digest": (
            operator_confirms_live_ticker_validation_candidate_review_package_digest
        ),
        "operator_confirms_ticker_universe_selection_approval_digest": (
            operator_confirms_ticker_universe_selection_approval_digest
        ),
        "operator_confirms_validation_target_universe": list(
            operator_confirms_validation_target_universe
        ),
        "operator_confirms_validation_target_count": operator_confirms_validation_target_count,
        "operator_confirms_approval_scope_read_only_provider_validation_only": (
            operator_confirms_approval_scope_read_only_provider_validation_only
        ),
        "operator_confirms_provider_request_authorized": (
            operator_confirms_provider_request_authorized
        ),
        "operator_confirms_live_ticker_validation_authorized": (
            operator_confirms_live_ticker_validation_authorized
        ),
        "operator_confirms_no_provider_requests_made_in_approval": (
            operator_confirms_no_provider_requests_made_in_approval
        ),
        "operator_confirms_no_live_provider_transport_enabled": (
            operator_confirms_no_live_provider_transport_enabled
        ),
        "operator_confirms_no_live_validation_performed": (
            operator_confirms_no_live_validation_performed
        ),
        "operator_confirms_no_validation_results_created": (
            operator_confirms_no_validation_results_created
        ),
        "operator_confirms_no_new_ticker_authority": operator_confirms_no_new_ticker_authority,
        "operator_confirms_no_new_ticker_acquisition": (
            operator_confirms_no_new_ticker_acquisition
        ),
        "operator_confirms_no_dataset_generation_authorization": (
            operator_confirms_no_dataset_generation_authorization
        ),
        "operator_confirms_no_additional_predictive_evidence_execution_authorization": (
            operator_confirms_no_additional_predictive_evidence_execution_authorization
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
        "operator_confirms_api_key_not_stored_or_printed": (
            operator_confirms_api_key_not_stored_or_printed
        ),
        "operator_confirms_raw_payload_not_committed": (
            operator_confirms_raw_payload_not_committed
        ),
    }


def _source_review_package(review_package: dict[str, Any] | None) -> dict[str, Any]:
    source_review = (
        deepcopy(review_package)
        if review_package is not None
        else review.build_live_ticker_validation_candidate_review_package_v1()
    )
    try:
        validation = review.validate_live_ticker_validation_candidate_review_package_v1(
            source_review
        )
    except review.LiveTickerValidationCandidateReviewPackageError as exc:
        raise LiveTickerValidationApprovalError(
            f"source live ticker validation candidate review package invalid: {exc}"
        ) from exc
    _expect(
        validation["live_ticker_validation_candidate_review_package_digest"],
        EXPECTED_LIVE_TICKER_VALIDATION_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "source live ticker validation candidate review package digest",
    )
    _expect(validation["failed_checks"], EXPECTED_REVIEW_CHECKLIST_FAILED, "source review failed check count")
    _expect(validation["blocker_count"], EXPECTED_REVIEW_BLOCKER_COUNT, "source review blocker count")
    return source_review


def _approval_target_entries(source_review: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "ticker": target["ticker"],
            "validation_approval_scope": READ_ONLY_PROVIDER_TICKER_VALIDATION_ONLY,
            "provider_request_authorized": True,
            "live_validation_authorized": True,
            "provider_request_status": NOT_REQUESTED,
            "live_validation_status": NOT_PERFORMED,
            "listing_status": NOT_VERIFIED,
            "security_type_status": NOT_VERIFIED,
            "exchange_status": NOT_VERIFIED,
            "active_status": NOT_VERIFIED,
            "delisting_status": NOT_VERIFIED,
            "tradability_status": NOT_VERIFIED,
            "corporate_action_data_availability_status": NOT_VERIFIED,
            "historical_aggregate_data_availability_status": NOT_VERIFIED,
            "identity_authority_status": NOT_CREATED,
            "split_event_authority_status": NOT_CREATED,
            "dividend_event_authority_status": NOT_CREATED,
            "acquisition_authority_status": NOT_CREATED,
            "canonical_dataset_authority_status": NOT_CREATED,
            "registry_approval_status": NOT_CREATED,
            "research_use_status": NOT_AUTHORIZED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
        }
        for target in source_review["validation_target_entries"]
    ]


def _review_evidence(source_review: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_live_ticker_validation_candidate_kind": source_review[
            "reviewed_live_ticker_validation_candidate_kind"
        ],
        "source_live_ticker_validation_candidate_status": source_review[
            "reviewed_live_ticker_validation_candidate_status"
        ],
        "source_live_ticker_validation_candidate_digest": source_review[
            "reviewed_live_ticker_validation_candidate_digest"
        ],
        "source_live_ticker_validation_candidate_review_package_kind": source_review[
            "artifact_kind"
        ],
        "source_live_ticker_validation_candidate_review_status": source_review[
            "review_status"
        ],
        "source_live_ticker_validation_candidate_review_package_digest": source_review[
            "live_ticker_validation_candidate_review_package_digest"
        ],
        "source_live_ticker_validation_candidate_review_checklist_total": source_review[
            "review_summary"
        ]["total_checks"],
        "source_live_ticker_validation_candidate_review_checklist_passed": source_review[
            "review_summary"
        ]["passed_checks"],
        "source_live_ticker_validation_candidate_review_checklist_failed": source_review[
            "review_summary"
        ]["failed_checks"],
        "source_live_ticker_validation_candidate_review_blocker_count": source_review[
            "review_summary"
        ]["blocker_count"],
        "ticker_universe_selection_approval_digest": source_review[
            "ticker_universe_selection_approval_digest"
        ],
        "ticker_universe_selection_approval_scope": source_review[
            "ticker_universe_selection_approval_scope"
        ],
        "ticker_universe_selection_candidate_digest": source_review[
            "ticker_universe_selection_candidate_digest"
        ],
        "ticker_universe_selection_candidate_review_package_digest": source_review[
            "ticker_universe_selection_candidate_review_package_digest"
        ],
        "predictive_evidence_scope_expansion_plan_candidate_review_package_digest": (
            source_review["predictive_evidence_scope_expansion_plan_candidate_review_package_digest"]
        ),
        "predictive_evidence_scope_expansion_plan_candidate_digest": source_review[
            "predictive_evidence_scope_expansion_plan_candidate_digest"
        ],
        "additional_predictive_evidence_plan_candidate_review_package_digest": source_review[
            "additional_predictive_evidence_plan_candidate_review_package_digest"
        ],
        "additional_predictive_evidence_plan_candidate_digest": source_review[
            "additional_predictive_evidence_plan_candidate_digest"
        ],
        "approved_expanded_ticker_universe": list(
            source_review["approved_expanded_ticker_universe"]
        ),
        "approved_expanded_ticker_count": source_review["approved_expanded_ticker_count"],
        "validation_target_universe": list(source_review["approved_expanded_ticker_universe"]),
        "validation_target_count": source_review["validation_target_count"],
        "validation_target_entries": _approval_target_entries(source_review),
    }


def _attestation_checks(attestation: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not isinstance(attestation, dict):
        return [
            _check("operator_decision_approved", OPERATOR_DECISION_APPROVE_LIVE_TICKER_VALIDATION, None),
            _check("operator_attestation_phrase_matches", REQUIRED_LIVE_TICKER_VALIDATION_APPROVAL_ATTESTATION_PHRASE, None),
            _check("operator_confirms_candidate_digest", EXPECTED_LIVE_TICKER_VALIDATION_CANDIDATE_DIGEST, None),
            _check("operator_confirms_candidate_review_digest", EXPECTED_LIVE_TICKER_VALIDATION_CANDIDATE_REVIEW_PACKAGE_DIGEST, None),
            _check("operator_confirms_ticker_universe_approval_digest", EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST, None),
            _check("operator_confirms_validation_target_universe", APPROVED_EXPANDED_TICKER_UNIVERSE, None),
            *[_check(field, True, None) for field in OPERATOR_CONFIRMATION_FIELDS],
        ]
    return [
        _check("operator_decision_approved", OPERATOR_DECISION_APPROVE_LIVE_TICKER_VALIDATION, attestation.get("operator_decision")),
        _check("operator_attestation_phrase_matches", REQUIRED_LIVE_TICKER_VALIDATION_APPROVAL_ATTESTATION_PHRASE, attestation.get("operator_attestation_phrase")),
        _check("operator_confirms_candidate_digest", EXPECTED_LIVE_TICKER_VALIDATION_CANDIDATE_DIGEST, attestation.get("operator_confirms_live_ticker_validation_candidate_digest")),
        _check("operator_confirms_candidate_review_digest", EXPECTED_LIVE_TICKER_VALIDATION_CANDIDATE_REVIEW_PACKAGE_DIGEST, attestation.get("operator_confirms_live_ticker_validation_candidate_review_package_digest")),
        _check("operator_confirms_ticker_universe_approval_digest", EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST, attestation.get("operator_confirms_ticker_universe_selection_approval_digest")),
        _check("operator_confirms_validation_target_universe", APPROVED_EXPANDED_TICKER_UNIVERSE, attestation.get("operator_confirms_validation_target_universe")),
        *[_check(field, True, attestation.get(field)) for field in OPERATOR_CONFIRMATION_FIELDS],
    ]


def _validated_operator_attestation(attestation: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(attestation, dict):
        raise LiveTickerValidationApprovalError("operator_attestation must be a JSON object")
    for field in (
        "operator_reference",
        "operator_attestation_timestamp_utc",
        "operator_attestation_version",
    ):
        value = attestation.get(field)
        if not isinstance(value, str) or not value.strip():
            raise LiveTickerValidationApprovalError(f"{field} must be a non-empty string")
    failed = [item for item in _attestation_checks(attestation) if item["status"] != PASS]
    if failed:
        raise LiveTickerValidationApprovalError(
            f"operator attestation failed: {failed[0]['check_id']}"
        )
    _expect(
        attestation.get("operator_confirms_validation_target_count"),
        12,
        "validation_target_count_12",
    )
    return deepcopy(attestation)


def _all_targets(artifact: dict[str, Any]) -> list[dict[str, Any]]:
    entries = artifact.get("validation_target_entries")
    return entries if isinstance(entries, list) else []


def _targets_have(field: str, expected: Any, artifact: dict[str, Any]) -> bool:
    targets = _all_targets(artifact)
    return bool(targets) and all(target.get(field) == expected for target in targets)


def _target_authorities_not_created(artifact: dict[str, Any]) -> bool:
    fields = (
        "identity_authority_status",
        "split_event_authority_status",
        "dividend_event_authority_status",
        "acquisition_authority_status",
        "canonical_dataset_authority_status",
        "registry_approval_status",
    )
    targets = _all_targets(artifact)
    return bool(targets) and all(
        target.get(field) == NOT_CREATED for target in targets for field in fields
    )


def _target_uses_not_authorized(artifact: dict[str, Any]) -> bool:
    fields = ("research_use_status", "runtime_use", "strategy_use", "paper_trading", "broker_execution")
    targets = _all_targets(artifact)
    return bool(targets) and all(
        target.get(field) == NOT_AUTHORIZED for target in targets for field in fields
    )


def _approval_checklist(approved: dict[str, Any]) -> list[dict[str, Any]]:
    target_tickers = [target.get("ticker") for target in _all_targets(approved)]
    return [
        _check("candidate_review_digest_matches_expected", EXPECTED_LIVE_TICKER_VALIDATION_CANDIDATE_REVIEW_PACKAGE_DIGEST, approved.get("source_live_ticker_validation_candidate_review_package_digest")),
        _check("candidate_review_has_zero_blockers", EXPECTED_REVIEW_BLOCKER_COUNT, approved.get("source_live_ticker_validation_candidate_review_blocker_count")),
        _check("candidate_digest_matches_expected", EXPECTED_LIVE_TICKER_VALIDATION_CANDIDATE_DIGEST, approved.get("source_live_ticker_validation_candidate_digest")),
        _check("ticker_universe_selection_approval_digest_matches_expected", EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST, approved.get("ticker_universe_selection_approval_digest")),
        _check("validation_target_universe_matches_expected", APPROVED_EXPANDED_TICKER_UNIVERSE, target_tickers),
        _check("validation_target_count_12", 12, approved.get("validation_target_count")),
        _check("approval_scope_read_only_provider_validation_only", READ_ONLY_PROVIDER_TICKER_VALIDATION_ONLY, approved.get("approval_scope")),
        *_attestation_checks(approved.get("operator_attestation") if isinstance(approved.get("operator_attestation"), dict) else None),
        _check("provider_request_authorized_true", True, approved.get("provider_request_authorized")),
        _check("live_ticker_validation_authorized_true", True, approved.get("live_ticker_validation_authorized")),
        _check("provider_requests_made_false", False, approved.get("provider_requests_made")),
        _check("provider_requests_made_in_approval_false", False, approved.get("provider_requests_made_in_approval")),
        _check("live_provider_transport_enabled_false", False, approved.get("live_provider_transport_enabled")),
        _check("live_ticker_validation_performed_false", False, approved.get("live_ticker_validation_performed")),
        _check("live_validation_results_created_false", False, approved.get("live_validation_results_created")),
        _check("validation_targets_provider_request_not_requested", True, _targets_have("provider_request_status", NOT_REQUESTED, approved)),
        _check("validation_targets_live_validation_not_performed", True, _targets_have("live_validation_status", NOT_PERFORMED, approved)),
        _check("validation_targets_listing_not_verified", True, _targets_have("listing_status", NOT_VERIFIED, approved)),
        _check("validation_targets_authority_not_created", True, _target_authorities_not_created(approved)),
        _check("validation_targets_runtime_not_authorized", True, _target_uses_not_authorized(approved)),
        _check("new_ticker_authority_created_false", False, approved.get("new_ticker_authority_created")),
        _check("new_ticker_acquisition_authorized_false", False, approved.get("new_ticker_acquisition_authorized")),
        _check("dataset_generation_authorized_false", False, approved.get("dataset_generation_authorized")),
        _check("additional_predictive_evidence_execution_authorized_false", False, approved.get("additional_predictive_evidence_execution_authorized")),
        _check("additional_predictive_evidence_executed_false", False, approved.get("additional_predictive_evidence_executed")),
        _check("predictive_experiment_rerun_authorized_false", False, approved.get("predictive_experiment_rerun_authorized")),
        _check("predictive_experiment_rerun_performed_false", False, approved.get("predictive_experiment_rerun_performed")),
        _check("walk_forward_rerun_performed_false", False, approved.get("walk_forward_rerun_performed")),
        _check("label_regeneration_performed_false", False, approved.get("label_regeneration_performed")),
        _check("feature_matrix_regeneration_performed_false", False, approved.get("feature_matrix_regeneration_performed")),
        _check("new_strategy_scoring_performed_false", False, approved.get("new_strategy_scoring_performed")),
        _check("trade_recommendations_generated_false", False, approved.get("trade_recommendations_generated")),
        _check("predictive_usefulness_not_accepted", acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED, approved.get("predictive_usefulness")),
        _check("predictive_usefulness_acceptance_ready_false", False, approved.get("predictive_usefulness_acceptance_ready")),
        _check("predictive_usefulness_acceptance_recommended_false", False, approved.get("predictive_usefulness_acceptance_recommended")),
        _check("predictive_usefulness_acceptance_candidate_created_false", False, approved.get("predictive_usefulness_acceptance_candidate_created")),
        _check("profitability_not_accepted", acquisition.PROFITABILITY_NOT_ACCEPTED, approved.get("profitability")),
        _check("profitability_acceptance_ready_false", False, approved.get("profitability_acceptance_ready")),
        _check("profitability_acceptance_recommended_false", False, approved.get("profitability_acceptance_recommended")),
        _check("runtime_migration_recommended_false", False, approved.get("runtime_migration_recommended")),
        _check("runtime_migration_approved_false", False, approved.get("runtime_migration_approved")),
        _check("runtime_migration_active_false", False, approved.get("runtime_migration_active")),
        _check("strategy_runtime_migration_false", False, approved.get("strategy_runtime_migration")),
        _check("runtime_use_not_authorized", NOT_AUTHORIZED, approved.get("runtime_use")),
        _check("strategy_use_not_authorized", NOT_AUTHORIZED, approved.get("strategy_use")),
        _check("paper_trading_not_authorized", NOT_AUTHORIZED, approved.get("paper_trading")),
        _check("broker_execution_not_authorized", NOT_AUTHORIZED, approved.get("broker_execution")),
        _check("automatic_stitching_false", False, approved.get("automatic_stitching")),
        _check("no_live_ticker_validation_execution_artifact_created", False, approved.get("live_ticker_validation_execution_artifact_created")),
        _check("no_live_validation_results_created", False, approved.get("live_validation_results_created")),
        _check("no_new_ticker_authority_artifact_created", False, approved.get("new_ticker_authority_artifact_created")),
        _check("no_acquisition_authorization_created", False, approved.get("acquisition_authorization_artifact_created")),
        _check("no_dataset_generation_authorization_created", False, approved.get("dataset_generation_authorization_created")),
        _check("no_predictive_usefulness_acceptance_artifact_created", False, approved.get("predictive_usefulness_acceptance_artifact_created")),
        _check("no_profitability_acceptance_created", False, approved.get("profitability_acceptance_artifact_created")),
        _check("no_runtime_migration_approval_created", False, approved.get("runtime_migration_approval_artifact_created")),
    ]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(checklist)
    passed = sum(1 for item in checklist if item["status"] == PASS)
    failed = total - passed
    blocker_count = sum(1 for item in checklist if item["status"] == FAIL and item["severity"] == BLOCKER)
    return {
        "total_checks": total,
        "passed_checks": passed,
        "failed_checks": failed,
        "blocker_count": blocker_count,
        "live_ticker_validation_authorized_by_operator": failed == 0,
        "provider_request_authorized": True,
        "provider_requests_made": False,
        "live_provider_transport_enabled": False,
        "live_ticker_validation_performed": False,
        "live_validation_results_created": False,
        "new_ticker_authority_authorized": False,
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
    payload.pop("live_ticker_validation_approval_digest", None)
    return payload


def live_ticker_validation_approval_digest_v1(approved_artifact: dict[str, Any]) -> str:
    """Return the deterministic semantic digest for a live ticker validation approval."""
    return semantic_digest(_digest_payload(approved_artifact))


def build_live_ticker_validation_approved_v1(
    *,
    live_ticker_validation_candidate_review_package: dict[str, Any] | None = None,
    operator_attestation: dict[str, Any],
) -> dict[str, Any]:
    """Build an offline approval artifact for future read-only provider validation."""
    source_review = _source_review_package(live_ticker_validation_candidate_review_package)
    attestation = _validated_operator_attestation(operator_attestation)
    approved = {
        "artifact_kind": ARTIFACT_KIND_LIVE_TICKER_VALIDATION_APPROVED,
        "schema_version": SCHEMA_VERSION_LIVE_TICKER_VALIDATION_APPROVAL_V1,
        "approval_status": LIVE_TICKER_VALIDATION_APPROVED,
        "approval_scope": READ_ONLY_PROVIDER_TICKER_VALIDATION_ONLY,
        "created_offline": True,
        "provider_request_authorized": True,
        "live_ticker_validation_authorized": True,
        "provider_requests_made": False,
        "provider_requests_made_in_approval": False,
        "live_provider_transport_enabled": False,
        "live_ticker_validation_performed": False,
        "live_validation_results_created": False,
        "ticker_universe_selection_approved": True,
        "expanded_ticker_universe_approved": True,
        "new_ticker_authority_created": False,
        "new_ticker_acquisition_authorized": False,
        "dataset_generation_authorized": False,
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
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "automatic_stitching": False,
        "live_ticker_validation_execution_artifact_created": False,
        "new_ticker_authority_artifact_created": False,
        "acquisition_authorization_artifact_created": False,
        "dataset_generation_authorization_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_artifact_created": False,
        "runtime_migration_approval_artifact_created": False,
        "api_key_handling": review.DO_NOT_STORE_KEYS_OR_PRINT_KEYS,
        "raw_payload_policy": review.DO_NOT_COMMIT_RAW_PROVIDER_PAYLOADS,
        "operator_attestation": attestation,
        "remaining_roadmap": list(REMAINING_ROADMAP_AFTER_LIVE_TICKER_VALIDATION_APPROVAL),
        **_review_evidence(source_review),
    }
    checklist = _approval_checklist(approved)
    approved["approval_checklist"] = checklist
    approved["approval_summary"] = _summary(checklist)
    approved["live_ticker_validation_approval_digest"] = (
        live_ticker_validation_approval_digest_v1(approved)
    )
    validate_live_ticker_validation_approved_v1(approved)
    return approved


def _reject_forbidden_values(mapping: dict[str, Any], *, path: str = "approved_artifact") -> None:
    forbidden_values = {
        "LIVE_TICKER_VALIDATION_PERFORMED",
        "LIVE_TICKER_VALIDATION_RESULTS",
        "NEW_TICKER_AUTHORITY_APPROVED",
        "NEW_TICKER_ACQUISITION_AUTHORIZED",
        "ACQUISITION_GENERATION_AUTHORIZED",
        "CANONICAL_DATASET_AUTHORIZED",
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
        "live_ticker_validation_performed",
        "live_validation_results_created",
        "new_ticker_authority_created",
        "new_ticker_acquisition_authorized",
        "dataset_generation_authorized",
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
        "live_ticker_validation_execution_artifact_created",
        "live_validation_results_created",
        "new_ticker_authority_artifact_created",
        "acquisition_authorization_artifact_created",
        "dataset_generation_authorization_created",
        "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_artifact_created",
        "runtime_migration_approval_artifact_created",
    }
    for key, value in mapping.items():
        current_path = f"{path}.{key}"
        if isinstance(value, str) and value in forbidden_values:
            raise LiveTickerValidationApprovalError(f"{current_path} must not emit {value}")
        if key in forbidden_true_fields and value is True:
            raise LiveTickerValidationApprovalError(f"{current_path} must be false")
        if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and value == "AUTHORIZED":
            raise LiveTickerValidationApprovalError(f"{current_path} must not be AUTHORIZED")
        if key in {"predictive_usefulness", "profitability"} and value == "accepted":
            raise LiveTickerValidationApprovalError(f"{current_path} must not be accepted")
        if isinstance(value, dict):
            _reject_forbidden_values(value, path=current_path)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, dict):
                    _reject_forbidden_values(item, path=f"{current_path}[{index}]")


def _validate_validation_targets(approved_artifact: dict[str, Any]) -> None:
    targets = approved_artifact.get("validation_target_entries")
    _expect(
        approved_artifact.get("validation_target_universe"),
        APPROVED_EXPANDED_TICKER_UNIVERSE,
        "validation_target_universe",
    )
    _expect(approved_artifact.get("validation_target_count"), 12, "validation_target_count")
    if not isinstance(targets, list) or len(targets) != 12:
        raise LiveTickerValidationApprovalError("validation_target_entries mismatch")
    if [target.get("ticker") for target in targets] != APPROVED_EXPANDED_TICKER_UNIVERSE:
        raise LiveTickerValidationApprovalError("validation target tickers mismatch")
    expected_statuses = {
        "validation_approval_scope": READ_ONLY_PROVIDER_TICKER_VALIDATION_ONLY,
        "provider_request_authorized": True,
        "live_validation_authorized": True,
        "provider_request_status": NOT_REQUESTED,
        "live_validation_status": NOT_PERFORMED,
        "listing_status": NOT_VERIFIED,
        "security_type_status": NOT_VERIFIED,
        "exchange_status": NOT_VERIFIED,
        "active_status": NOT_VERIFIED,
        "delisting_status": NOT_VERIFIED,
        "tradability_status": NOT_VERIFIED,
        "corporate_action_data_availability_status": NOT_VERIFIED,
        "historical_aggregate_data_availability_status": NOT_VERIFIED,
        "identity_authority_status": NOT_CREATED,
        "split_event_authority_status": NOT_CREATED,
        "dividend_event_authority_status": NOT_CREATED,
        "acquisition_authority_status": NOT_CREATED,
        "canonical_dataset_authority_status": NOT_CREATED,
        "registry_approval_status": NOT_CREATED,
        "research_use_status": NOT_AUTHORIZED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
    }
    for target in targets:
        ticker = target.get("ticker")
        for field, expected in expected_statuses.items():
            _expect(target.get(field), expected, f"validation_target_entries.{ticker}.{field}")


def validate_live_ticker_validation_approved_v1(
    approved_artifact: dict[str, Any],
) -> dict[str, Any]:
    """Validate approval while preserving all execution and runtime guardrails."""
    if not isinstance(approved_artifact, dict):
        raise LiveTickerValidationApprovalError("approved artifact must be a JSON object")
    _reject_forbidden_values(approved_artifact)
    for field, expected in {
        "artifact_kind": ARTIFACT_KIND_LIVE_TICKER_VALIDATION_APPROVED,
        "schema_version": SCHEMA_VERSION_LIVE_TICKER_VALIDATION_APPROVAL_V1,
        "approval_status": LIVE_TICKER_VALIDATION_APPROVED,
        "approval_scope": READ_ONLY_PROVIDER_TICKER_VALIDATION_ONLY,
    }.items():
        _expect(approved_artifact.get(field), expected, field)
    for field in (
        "created_offline",
        "provider_request_authorized",
        "live_ticker_validation_authorized",
        "ticker_universe_selection_approved",
        "expanded_ticker_universe_approved",
        "research_only",
    ):
        _expect_true(approved_artifact.get(field), field)
    for field in (
        "provider_requests_made",
        "provider_requests_made_in_approval",
        "live_provider_transport_enabled",
        "live_ticker_validation_performed",
        "live_validation_results_created",
        "new_ticker_authority_created",
        "new_ticker_acquisition_authorized",
        "dataset_generation_authorized",
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
        "live_ticker_validation_execution_artifact_created",
        "new_ticker_authority_artifact_created",
        "acquisition_authorization_artifact_created",
        "dataset_generation_authorization_created",
        "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_artifact_created",
        "runtime_migration_approval_artifact_created",
    ):
        _expect_false(approved_artifact.get(field), field)
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(approved_artifact.get(field), NOT_AUTHORIZED, field)
    for field, expected in {
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "source_live_ticker_validation_candidate_kind": (
            review.candidate_service.ARTIFACT_KIND_LIVE_TICKER_VALIDATION_CANDIDATE
        ),
        "source_live_ticker_validation_candidate_status": (
            review.candidate_service.LIVE_TICKER_VALIDATION_READY_FOR_OPERATOR_REVIEW
        ),
        "source_live_ticker_validation_candidate_digest": (
            EXPECTED_LIVE_TICKER_VALIDATION_CANDIDATE_DIGEST
        ),
        "source_live_ticker_validation_candidate_review_package_kind": (
            review.ARTIFACT_KIND_LIVE_TICKER_VALIDATION_CANDIDATE_REVIEW_PACKAGE
        ),
        "source_live_ticker_validation_candidate_review_status": (
            review.LIVE_TICKER_VALIDATION_CANDIDATE_REVIEW_PACKAGE_READY
        ),
        "source_live_ticker_validation_candidate_review_package_digest": (
            EXPECTED_LIVE_TICKER_VALIDATION_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "source_live_ticker_validation_candidate_review_checklist_failed": 0,
        "source_live_ticker_validation_candidate_review_blocker_count": 0,
        "ticker_universe_selection_approval_digest": (
            EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST
        ),
        "ticker_universe_selection_approval_scope": (
            review.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_SCOPE
        ),
        "ticker_universe_selection_candidate_digest": (
            review.EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_DIGEST
        ),
        "ticker_universe_selection_candidate_review_package_digest": (
            review.EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "predictive_evidence_scope_expansion_plan_candidate_review_package_digest": (
            review.EXPECTED_SCOPE_EXPANSION_REVIEW_PACKAGE_DIGEST
        ),
        "predictive_evidence_scope_expansion_plan_candidate_digest": (
            review.EXPECTED_SCOPE_EXPANSION_CANDIDATE_DIGEST
        ),
        "additional_predictive_evidence_plan_candidate_review_package_digest": (
            review.EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_REVIEW_PACKAGE_DIGEST
        ),
        "additional_predictive_evidence_plan_candidate_digest": (
            review.EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE_DIGEST
        ),
        "approved_expanded_ticker_universe": APPROVED_EXPANDED_TICKER_UNIVERSE,
        "approved_expanded_ticker_count": 12,
        "api_key_handling": review.DO_NOT_STORE_KEYS_OR_PRINT_KEYS,
        "raw_payload_policy": review.DO_NOT_COMMIT_RAW_PROVIDER_PAYLOADS,
        "remaining_roadmap": REMAINING_ROADMAP_AFTER_LIVE_TICKER_VALIDATION_APPROVAL,
    }.items():
        _expect(approved_artifact.get(field), expected, field)
    _validate_validation_targets(approved_artifact)
    _validated_operator_attestation(approved_artifact.get("operator_attestation"))
    checklist = _approval_checklist(approved_artifact)
    _expect([item["check_id"] for item in checklist], REQUIRED_APPROVAL_CHECK_IDS, "approval_checklist check IDs")
    failed = [item for item in checklist if item["status"] != PASS]
    if failed:
        raise LiveTickerValidationApprovalError(
            f"approval checklist contains failed check: {failed[0]['check_id']}"
        )
    _expect(approved_artifact.get("approval_checklist"), checklist, "approval_checklist")
    summary = _summary(checklist)
    _expect(approved_artifact.get("approval_summary"), summary, "approval_summary")
    digest = approved_artifact.get("live_ticker_validation_approval_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise LiveTickerValidationApprovalError("live_ticker_validation_approval_digest missing")
    _expect(
        digest,
        live_ticker_validation_approval_digest_v1(approved_artifact),
        "live_ticker_validation_approval_digest",
    )
    return {
        "status": "LIVE_TICKER_VALIDATION_APPROVED_VALID",
        "artifact_kind": approved_artifact["artifact_kind"],
        "approval_status": approved_artifact["approval_status"],
        "approval_scope": approved_artifact["approval_scope"],
        "live_ticker_validation_approval_digest": digest,
        "source_live_ticker_validation_candidate_digest": (
            EXPECTED_LIVE_TICKER_VALIDATION_CANDIDATE_DIGEST
        ),
        "source_live_ticker_validation_candidate_review_package_digest": (
            EXPECTED_LIVE_TICKER_VALIDATION_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "ticker_universe_selection_approval_digest": (
            EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST
        ),
        "validation_target_universe": list(APPROVED_EXPANDED_TICKER_UNIVERSE),
        "validation_target_count": 12,
        "provider_request_authorized": True,
        "live_ticker_validation_authorized": True,
        "provider_requests_made": False,
        "provider_requests_made_in_approval": False,
        "live_provider_transport_enabled": False,
        "live_ticker_validation_performed": False,
        "live_validation_results_created": False,
        "new_ticker_authority_created": False,
        "new_ticker_acquisition_authorized": False,
        "dataset_generation_authorized": False,
        "additional_predictive_evidence_execution_authorized": False,
        "additional_predictive_evidence_executed": False,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "runtime_migration_approved": False,
        "runtime_migration_active": False,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "total_checks": summary["total_checks"],
        "passed_checks": summary["passed_checks"],
        "failed_checks": summary["failed_checks"],
        "blocker_count": summary["blocker_count"],
    }


def build_live_ticker_validation_approved_markdown_v1(
    approved_artifact: dict[str, Any],
) -> str:
    """Render a sanitized live ticker validation approval status document."""
    validation = validate_live_ticker_validation_approved_v1(approved_artifact)
    attestation = approved_artifact["operator_attestation"]
    summary = approved_artifact["approval_summary"]
    lines = [
        "# MarketFlow Live Ticker Validation Approval Status",
        "",
        "## Title",
        "- Live Ticker Validation Approval Ceremony v1.",
        "",
        "## Approved Live Ticker Validation",
        f"- Artifact kind: `{approved_artifact['artifact_kind']}`",
        f"- Approval status: `{approved_artifact['approval_status']}`",
        f"- Approval scope: `{approved_artifact['approval_scope']}`",
        f"- Approval digest: `{validation['live_ticker_validation_approval_digest']}`",
        f"- Provider request authorized: `{approved_artifact['provider_request_authorized']}`",
        f"- Live ticker validation authorized: `{approved_artifact['live_ticker_validation_authorized']}`",
        "",
        "## Operator Attestation",
        f"- Operator reference: `{attestation['operator_reference']}`",
        f"- Operator decision: `{attestation['operator_decision']}`",
        f"- Attestation timestamp UTC: `{attestation['operator_attestation_timestamp_utc']}`",
        f"- Attestation version: `{attestation['operator_attestation_version']}`",
        "",
        "## Source Candidate Review Package",
        f"- Review package kind: `{approved_artifact['source_live_ticker_validation_candidate_review_package_kind']}`",
        f"- Review status: `{approved_artifact['source_live_ticker_validation_candidate_review_status']}`",
        f"- Review package digest: `{approved_artifact['source_live_ticker_validation_candidate_review_package_digest']}`",
        f"- Candidate digest: `{approved_artifact['source_live_ticker_validation_candidate_digest']}`",
        f"- Review blockers: `{approved_artifact['source_live_ticker_validation_candidate_review_blocker_count']}`",
        "",
        "## Validation Target Universe",
        f"- Validation target count: `{approved_artifact['validation_target_count']}`",
        "- Validation targets: "
        + ", ".join(f"`{ticker}`" for ticker in approved_artifact["validation_target_universe"]),
        "",
        "## Approval Scope",
        f"- approval_scope: `{approved_artifact['approval_scope']}`",
        "- This approval is limited to future read-only provider ticker validation.",
        "",
        "## Provider Request Boundary",
        f"- provider_request_authorized: `{approved_artifact['provider_request_authorized']}`",
        f"- provider_requests_made: `{approved_artifact['provider_requests_made']}`",
        f"- provider_requests_made_in_approval: `{approved_artifact['provider_requests_made_in_approval']}`",
        "",
        "## API Key / Raw Payload Boundary",
        f"- api_key_handling: `{approved_artifact['api_key_handling']}`",
        f"- raw_payload_policy: `{approved_artifact['raw_payload_policy']}`",
        "",
        "## Validation Execution Boundary",
        f"- live_provider_transport_enabled: `{approved_artifact['live_provider_transport_enabled']}`",
        f"- live_ticker_validation_performed: `{approved_artifact['live_ticker_validation_performed']}`",
        f"- live_validation_results_created: `{approved_artifact['live_validation_results_created']}`",
        "",
        "## New Ticker Authority Boundary",
        f"- new_ticker_authority_created: `{approved_artifact['new_ticker_authority_created']}`",
        f"- new_ticker_authority_artifact_created: `{approved_artifact['new_ticker_authority_artifact_created']}`",
        "",
        "## Acquisition Boundary",
        f"- new_ticker_acquisition_authorized: `{approved_artifact['new_ticker_acquisition_authorized']}`",
        f"- acquisition_authorization_artifact_created: `{approved_artifact['acquisition_authorization_artifact_created']}`",
        f"- dataset_generation_authorized: `{approved_artifact['dataset_generation_authorized']}`",
        "",
        "## Predictive/Profitability Boundary",
        f"- additional_predictive_evidence_execution_authorized: `{approved_artifact['additional_predictive_evidence_execution_authorized']}`",
        f"- additional_predictive_evidence_executed: `{approved_artifact['additional_predictive_evidence_executed']}`",
        f"- predictive_usefulness: `{approved_artifact['predictive_usefulness']}`",
        f"- profitability: `{approved_artifact['profitability']}`",
        "",
        "## Runtime Boundary",
        f"- runtime_migration_recommended: `{approved_artifact['runtime_migration_recommended']}`",
        f"- runtime_migration_approved: `{approved_artifact['runtime_migration_approved']}`",
        f"- runtime_migration_active: `{approved_artifact['runtime_migration_active']}`",
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
    lines.extend(f"{index}. {task}" for index, task in enumerate(approved_artifact["remaining_roadmap"], start=1))
    lines.extend(
        [
            "",
            "## Guardrails",
            "- Created offline: `True`",
            "- No provider request was made by this approval ceremony.",
            "- No live provider transport was enabled.",
            "- No live ticker validation was performed.",
            "- No validation results were created.",
            "- No new ticker authority, acquisition, dataset generation, predictive acceptance, profitability acceptance, runtime activation, paper trading, broker execution, or trade recommendation artifact was created.",
            "",
        ]
    )
    return "\n".join(lines)


def write_live_ticker_validation_approved_v1(
    output_dir: str | Path,
    *,
    live_ticker_validation_candidate_review_package: dict[str, Any] | None = None,
    operator_attestation: dict[str, Any],
    filename: str | None = None,
) -> dict[str, Any]:
    """Write the live ticker validation approval JSON artifact without overwriting output."""
    approved = build_live_ticker_validation_approved_v1(
        live_ticker_validation_candidate_review_package=live_ticker_validation_candidate_review_package,
        operator_attestation=operator_attestation,
    )
    validation = validate_live_ticker_validation_approved_v1(approved)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "live_ticker_validation_approved_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise LiveTickerValidationApprovalError(
            "live ticker validation approval filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise LiveTickerValidationApprovalError(
            f"live ticker validation approval output already exists: {_path_text(path)}"
        )
    payload = canonical_json_bytes(approved)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": _path_text(path),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
    }
