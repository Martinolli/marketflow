"""Offline identity-only freeze ceremony for the expanded-universe ticker identities."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import expanded_universe_per_ticker_identity_authority_candidate_service as candidate_service
from marketflow.services import (
    expanded_universe_per_ticker_identity_authority_candidate_operator_review_service as review_service,
)


ARTIFACT_KIND_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_FROZEN = (
    "EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_FROZEN"
)
SCHEMA_VERSION_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_FREEZE_V1 = (
    "expanded_universe_per_ticker_identity_authority_freeze_v1"
)
EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_FROZEN = (
    "EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_FROZEN"
)
IDENTITY_AUTHORITY_ONLY = "IDENTITY_AUTHORITY_ONLY"
IDENTITY_FREEZE_STATUS_FROZEN = "FROZEN"
OPERATOR_DECISION_FREEZE_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY = (
    "FREEZE_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY"
)
OPERATOR_ATTESTATION_VERSION_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_FREEZE_V1 = (
    "expanded_universe_per_ticker_identity_authority_freeze_attestation_v1"
)
REQUIRED_OPERATOR_ATTESTATION_PHRASE = (
    "FREEZE EXPANDED UNIVERSE PER TICKER IDENTITY AUTHORITY "
    "MSFT NVDA AMZN GOOGL META TSLA JPM XOM JNJ WMT CAT LMT "
    "IDENTITY_AUTHORITY_ONLY"
)

EXPECTED_IDENTITY_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    "31f010bb328dd71f578ea5c99cc1cb54332a6840d9693b373b73ac688ee118eb"
)
EXPECTED_IDENTITY_AUTHORITY_CANDIDATE_DIGEST = (
    review_service.EXPECTED_IDENTITY_AUTHORITY_CANDIDATE_DIGEST
)
EXPECTED_IDENTITY_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    candidate_service.EXPECTED_IDENTITY_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST
)
EXPECTED_IDENTITY_AUTHORITY_PLAN_CANDIDATE_DIGEST = (
    candidate_service.EXPECTED_IDENTITY_AUTHORITY_PLAN_CANDIDATE_DIGEST
)
EXPECTED_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_DIGEST = (
    candidate_service.plan_review.plan.EXPECTED_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_DIGEST
)
EXPECTED_LIVE_TICKER_VALIDATION_EXECUTION_DIGEST = (
    candidate_service.plan_review.plan.EXPECTED_LIVE_TICKER_VALIDATION_EXECUTION_DIGEST
)
EXPECTED_LIVE_TICKER_VALIDATION_APPROVAL_DIGEST = (
    candidate_service.plan_review.plan.EXPECTED_LIVE_TICKER_VALIDATION_APPROVAL_DIGEST
)
EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST = (
    candidate_service.plan_review.plan.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST
)

VALIDATION_TARGET_UNIVERSE = list(review_service.VALIDATION_TARGET_UNIVERSE)
IDENTITY_FIELDS_TO_BIND = list(review_service.IDENTITY_FIELDS_TO_BIND)
IDENTITY_EVIDENCE_LIMITATIONS = list(review_service.IDENTITY_EVIDENCE_LIMITATIONS)
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

REMAINING_REQUIRED_TASKS = [
    "post_identity_freeze_registry_inventory_candidate",
    "corporate_action_authority_chain_candidate",
    "acquisition_generation_chain_candidate",
    "canonical_dataset_chain_candidate",
    "research_registry_chain_candidate",
]

REQUIRED_TRUE_ATTESTATION_FIELDS = [
    "operator_confirms_authority_scope_identity_only",
    "operator_confirms_per_ticker_identity_entries_reviewed",
    "operator_confirms_no_provider_requests_in_freeze",
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
    "identity_candidate_review_digest_matches_expected",
    "identity_candidate_review_has_zero_blockers",
    "identity_candidate_digest_matches_expected",
    "identity_plan_review_digest_matches_expected",
    "live_validation_results_review_digest_matches_expected",
    "target_universe_count_12",
    "target_universe_matches_reviewed_universe",
    "operator_decision_freeze",
    "operator_attestation_phrase_matches",
    "operator_confirms_identity_candidate_review_digest",
    "operator_confirms_identity_candidate_digest",
    "operator_confirms_identity_plan_review_digest",
    "operator_confirms_live_validation_results_review_digest",
    "operator_confirms_target_universe",
    "operator_confirms_target_count",
    "operator_confirms_authority_scope_identity_only",
    "operator_confirms_per_ticker_identity_entries_reviewed",
    "operator_confirms_no_provider_requests",
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
    "authority_scope_identity_only",
    "per_ticker_identity_authority_frozen_true",
    "identity_authority_created_true",
    "identity_authority_frozen_true",
    "new_ticker_identity_authority_created_true",
    "per_ticker_frozen_entries_12",
    "per_ticker_freeze_digests_present",
    "unavailable_fields_preserved_as_unavailable",
    "no_unavailable_fields_fabricated",
    "provider_requests_made_in_freeze_false",
    "live_validation_rerun_performed_false",
    "live_provider_transport_enabled_in_freeze_false",
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


class ExpandedUniversePerTickerIdentityAuthorityFreezeError(ValueError):
    """Raised when the expanded-universe identity authority freeze is invalid."""


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
        raise ExpandedUniversePerTickerIdentityAuthorityFreezeError(f"{field_name} mismatch")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise ExpandedUniversePerTickerIdentityAuthorityFreezeError(f"{field_name} must be true")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise ExpandedUniversePerTickerIdentityAuthorityFreezeError(f"{field_name} must be false")


def _path_text(path: Path) -> str:
    return str(path).replace("\\", "/")


def build_expanded_universe_per_ticker_identity_authority_freeze_attestation_v1(
    *,
    operator_reference: str,
    operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str,
    operator_confirms_identity_candidate_review_package_digest: str,
    operator_confirms_identity_candidate_digest: str,
    operator_confirms_identity_plan_review_package_digest: str,
    operator_confirms_live_validation_results_review_digest: str,
    operator_confirms_target_universe: list[str],
    operator_confirms_target_count: int,
    operator_confirms_authority_scope_identity_only: bool,
    operator_confirms_per_ticker_identity_entries_reviewed: bool,
    operator_confirms_no_provider_requests_in_freeze: bool,
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
    operator_decision: str = OPERATOR_DECISION_FREEZE_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY,
) -> dict[str, Any]:
    """Build the non-secret operator attestation required for the freeze ceremony."""
    return {
        "operator_decision": operator_decision,
        "operator_attestation_phrase": operator_attestation_phrase,
        "operator_attestation_timestamp_utc": operator_attestation_timestamp_utc,
        "operator_attestation_version": (
            OPERATOR_ATTESTATION_VERSION_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_FREEZE_V1
        ),
        "operator_reference": operator_reference,
        "operator_confirms_identity_candidate_review_package_digest": (
            operator_confirms_identity_candidate_review_package_digest
        ),
        "operator_confirms_identity_candidate_digest": (
            operator_confirms_identity_candidate_digest
        ),
        "operator_confirms_identity_plan_review_package_digest": (
            operator_confirms_identity_plan_review_package_digest
        ),
        "operator_confirms_live_validation_results_review_digest": (
            operator_confirms_live_validation_results_review_digest
        ),
        "operator_confirms_target_universe": list(operator_confirms_target_universe),
        "operator_confirms_target_count": operator_confirms_target_count,
        "operator_confirms_authority_scope_identity_only": (
            operator_confirms_authority_scope_identity_only
        ),
        "operator_confirms_per_ticker_identity_entries_reviewed": (
            operator_confirms_per_ticker_identity_entries_reviewed
        ),
        "operator_confirms_no_provider_requests_in_freeze": (
            operator_confirms_no_provider_requests_in_freeze
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


def _validate_operator_attestation(
    operator_attestation: dict[str, Any],
    review_package: dict[str, Any],
) -> None:
    if not isinstance(operator_attestation, dict):
        raise ExpandedUniversePerTickerIdentityAuthorityFreezeError(
            "operator_attestation must be a JSON object"
        )
    _expect(
        operator_attestation.get("operator_decision"),
        OPERATOR_DECISION_FREEZE_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY,
        "operator_decision",
    )
    _expect(
        operator_attestation.get("operator_attestation_phrase"),
        REQUIRED_OPERATOR_ATTESTATION_PHRASE,
        "operator_attestation_phrase",
    )
    _expect(
        operator_attestation.get("operator_attestation_version"),
        OPERATOR_ATTESTATION_VERSION_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_FREEZE_V1,
        "operator_attestation_version",
    )
    if not operator_attestation.get("operator_reference"):
        raise ExpandedUniversePerTickerIdentityAuthorityFreezeError("operator_reference missing")
    if not operator_attestation.get("operator_attestation_timestamp_utc"):
        raise ExpandedUniversePerTickerIdentityAuthorityFreezeError(
            "operator_attestation_timestamp_utc missing"
        )
    _expect(
        operator_attestation.get("operator_confirms_identity_candidate_review_package_digest"),
        review_package[
            "expanded_universe_per_ticker_identity_authority_candidate_review_package_digest"
        ],
        "operator_confirms_identity_candidate_review_package_digest",
    )
    _expect(
        operator_attestation.get("operator_confirms_identity_candidate_digest"),
        review_package["identity_authority_candidate_digest"],
        "operator_confirms_identity_candidate_digest",
    )
    _expect(
        operator_attestation.get("operator_confirms_identity_plan_review_package_digest"),
        review_package["identity_authority_plan_candidate_review_package_digest"],
        "operator_confirms_identity_plan_review_package_digest",
    )
    _expect(
        operator_attestation.get("operator_confirms_live_validation_results_review_digest"),
        review_package["live_ticker_validation_results_review_package_digest"],
        "operator_confirms_live_validation_results_review_digest",
    )
    _expect(
        operator_attestation.get("operator_confirms_target_universe"),
        VALIDATION_TARGET_UNIVERSE,
        "operator_confirms_target_universe",
    )
    _expect(
        operator_attestation.get("operator_confirms_target_count"),
        12,
        "operator_confirms_target_count",
    )
    for field in REQUIRED_TRUE_ATTESTATION_FIELDS:
        _expect_true(operator_attestation.get(field), field)


def _per_ticker_identity_freeze_digest_payload(entry: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(entry)
    payload.pop("per_ticker_identity_freeze_digest", None)
    return payload


def per_ticker_identity_freeze_digest_v1(entry: dict[str, Any]) -> str:
    """Return the deterministic semantic digest for one frozen identity entry."""
    return semantic_digest(_per_ticker_identity_freeze_digest_payload(entry))


def _identity_field_status_summary(identity_fields: dict[str, Any]) -> dict[str, int]:
    summary: dict[str, int] = {}
    for field in identity_fields.values():
        if isinstance(field, dict):
            status = field.get("status")
            if isinstance(status, str):
                summary[status] = summary.get(status, 0) + 1
    return dict(sorted(summary.items()))


def _frozen_entries(review_package: dict[str, Any]) -> list[dict[str, Any]]:
    candidate_by_ticker = {
        entry.get("ticker"): entry
        for entry in review_package.get("per_ticker_identity_candidate_entries", [])
        if isinstance(entry, dict)
    }
    entries: list[dict[str, Any]] = []
    for review_entry in review_package.get("per_ticker_identity_review_entries", []):
        ticker = review_entry.get("ticker")
        candidate_entry = candidate_by_ticker.get(ticker, {})
        identity_fields = deepcopy(review_entry.get("identity_fields", {}))
        entry = {
            "ticker": ticker,
            "live_validation_status": candidate_entry.get("live_validation_status"),
            "identity_candidate_status": review_entry.get("identity_candidate_status"),
            "identity_review_status": review_entry.get("identity_review_status"),
            "identity_freeze_status": IDENTITY_FREEZE_STATUS_FROZEN,
            "identity_authority_scope": IDENTITY_AUTHORITY_ONLY,
            "identity_authority_created": True,
            "identity_authority_frozen": True,
            "corporate_action_authority_created": False,
            "acquisition_authority_created": False,
            "dataset_generation_authorized": False,
            "runtime_use": candidate_service.plan_review.plan.NOT_AUTHORIZED,
            "strategy_use": candidate_service.plan_review.plan.NOT_AUTHORIZED,
            "paper_trading": candidate_service.plan_review.plan.NOT_AUTHORIZED,
            "broker_execution": candidate_service.plan_review.plan.NOT_AUTHORIZED,
            "frozen_identity_fields": identity_fields,
            "identity_field_status_summary": _identity_field_status_summary(identity_fields),
            "unavailable_fields_preserved_as_unavailable": True,
            "identity_evidence_limitations": list(
                review_entry.get("identity_evidence_limitations", [])
            ),
            "source_per_ticker_identity_candidate_digest": review_entry.get(
                "per_ticker_identity_candidate_digest"
            ),
            "source_per_ticker_identity_review_digest": review_entry.get(
                "per_ticker_identity_review_digest"
            ),
        }
        entry["per_ticker_identity_freeze_digest"] = per_ticker_identity_freeze_digest_v1(
            entry
        )
        entries.append(entry)
    return entries


def _freeze_entries_from_artifact(frozen_artifact: dict[str, Any]) -> list[dict[str, Any]]:
    entries = frozen_artifact.get("per_ticker_frozen_identity_entries")
    return entries if isinstance(entries, list) else []


def _identity_fields_have_value_status(entries: list[dict[str, Any]]) -> bool:
    for entry in entries:
        fields = entry.get("frozen_identity_fields")
        if not isinstance(fields, dict):
            return False
        for field in IDENTITY_FIELDS_TO_BIND:
            value = fields.get(field)
            if not isinstance(value, dict) or set(value) != {"value", "status"}:
                return False
    return True


def _unavailable_fields_not_fabricated(entries: list[dict[str, Any]]) -> bool:
    for entry in entries:
        fields = entry.get("frozen_identity_fields")
        if not isinstance(fields, dict):
            return False
        for value in fields.values():
            if (
                isinstance(value, dict)
                and value.get("status") == candidate_service.UNAVAILABLE_IN_SOURCE
                and value.get("value") is not None
            ):
                return False
    return True


def _per_ticker_freeze_digests_present(entries: list[dict[str, Any]]) -> bool:
    return all(
        isinstance(entry.get("per_ticker_identity_freeze_digest"), str)
        and len(entry["per_ticker_identity_freeze_digest"]) == 64
        for entry in entries
    )


def _checklist(frozen_artifact: dict[str, Any]) -> list[dict[str, Any]]:
    operator_attestation = frozen_artifact.get("operator_attestation", {})
    entries = _freeze_entries_from_artifact(frozen_artifact)
    return [
        _check(
            "identity_candidate_review_digest_matches_expected",
            EXPECTED_IDENTITY_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
            frozen_artifact.get("identity_authority_candidate_review_package_digest"),
        ),
        _check("identity_candidate_review_has_zero_blockers", 0, frozen_artifact.get("review_blocker_count")),
        _check(
            "identity_candidate_digest_matches_expected",
            EXPECTED_IDENTITY_AUTHORITY_CANDIDATE_DIGEST,
            frozen_artifact.get("identity_authority_candidate_digest"),
        ),
        _check(
            "identity_plan_review_digest_matches_expected",
            EXPECTED_IDENTITY_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST,
            frozen_artifact.get("identity_authority_plan_candidate_review_package_digest"),
        ),
        _check(
            "live_validation_results_review_digest_matches_expected",
            EXPECTED_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_DIGEST,
            frozen_artifact.get("live_ticker_validation_results_review_package_digest"),
        ),
        _check("target_universe_count_12", 12, frozen_artifact.get("target_universe_count")),
        _check(
            "target_universe_matches_reviewed_universe",
            VALIDATION_TARGET_UNIVERSE,
            frozen_artifact.get("target_universe"),
        ),
        _check(
            "operator_decision_freeze",
            OPERATOR_DECISION_FREEZE_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY,
            operator_attestation.get("operator_decision"),
        ),
        _check(
            "operator_attestation_phrase_matches",
            REQUIRED_OPERATOR_ATTESTATION_PHRASE,
            operator_attestation.get("operator_attestation_phrase"),
        ),
        _check(
            "operator_confirms_identity_candidate_review_digest",
            frozen_artifact.get("identity_authority_candidate_review_package_digest"),
            operator_attestation.get("operator_confirms_identity_candidate_review_package_digest"),
        ),
        _check(
            "operator_confirms_identity_candidate_digest",
            frozen_artifact.get("identity_authority_candidate_digest"),
            operator_attestation.get("operator_confirms_identity_candidate_digest"),
        ),
        _check(
            "operator_confirms_identity_plan_review_digest",
            frozen_artifact.get("identity_authority_plan_candidate_review_package_digest"),
            operator_attestation.get("operator_confirms_identity_plan_review_package_digest"),
        ),
        _check(
            "operator_confirms_live_validation_results_review_digest",
            frozen_artifact.get("live_ticker_validation_results_review_package_digest"),
            operator_attestation.get("operator_confirms_live_validation_results_review_digest"),
        ),
        _check(
            "operator_confirms_target_universe",
            VALIDATION_TARGET_UNIVERSE,
            operator_attestation.get("operator_confirms_target_universe"),
        ),
        _check("operator_confirms_target_count", 12, operator_attestation.get("operator_confirms_target_count")),
        _check(
            "operator_confirms_authority_scope_identity_only",
            True,
            operator_attestation.get("operator_confirms_authority_scope_identity_only"),
        ),
        _check(
            "operator_confirms_per_ticker_identity_entries_reviewed",
            True,
            operator_attestation.get("operator_confirms_per_ticker_identity_entries_reviewed"),
        ),
        _check(
            "operator_confirms_no_provider_requests",
            True,
            operator_attestation.get("operator_confirms_no_provider_requests_in_freeze"),
        ),
        _check(
            "operator_confirms_no_live_validation_rerun",
            True,
            operator_attestation.get("operator_confirms_no_live_validation_rerun"),
        ),
        _check(
            "operator_confirms_no_live_provider_transport_enabled",
            True,
            operator_attestation.get("operator_confirms_no_live_provider_transport_enabled"),
        ),
        _check(
            "operator_confirms_no_corporate_action_authority",
            True,
            operator_attestation.get("operator_confirms_no_corporate_action_authority"),
        ),
        _check(
            "operator_confirms_no_split_event_authority",
            True,
            operator_attestation.get("operator_confirms_no_split_event_authority"),
        ),
        _check(
            "operator_confirms_no_dividend_event_authority",
            True,
            operator_attestation.get("operator_confirms_no_dividend_event_authority"),
        ),
        _check(
            "operator_confirms_no_acquisition_authority",
            True,
            operator_attestation.get("operator_confirms_no_acquisition_authority"),
        ),
        _check(
            "operator_confirms_no_dataset_generation_authorization",
            True,
            operator_attestation.get("operator_confirms_no_dataset_generation_authorization"),
        ),
        _check(
            "operator_confirms_no_additional_predictive_evidence_execution",
            True,
            operator_attestation.get("operator_confirms_no_additional_predictive_evidence_execution"),
        ),
        _check(
            "operator_confirms_no_predictive_usefulness_acceptance",
            True,
            operator_attestation.get("operator_confirms_no_predictive_usefulness_acceptance"),
        ),
        _check(
            "operator_confirms_no_profitability_acceptance",
            True,
            operator_attestation.get("operator_confirms_no_profitability_acceptance"),
        ),
        _check(
            "operator_confirms_no_runtime_migration_approval",
            True,
            operator_attestation.get("operator_confirms_no_runtime_migration_approval"),
        ),
        _check(
            "operator_confirms_no_runtime_activation",
            True,
            operator_attestation.get("operator_confirms_no_runtime_activation"),
        ),
        _check(
            "operator_confirms_no_paper_trading",
            True,
            operator_attestation.get("operator_confirms_no_paper_trading"),
        ),
        _check(
            "operator_confirms_no_broker_execution",
            True,
            operator_attestation.get("operator_confirms_no_broker_execution"),
        ),
        _check(
            "operator_confirms_no_trade_recommendations",
            True,
            operator_attestation.get("operator_confirms_no_trade_recommendations"),
        ),
        _check(
            "operator_confirms_no_api_key_storage_or_printing",
            True,
            operator_attestation.get("operator_confirms_no_api_key_storage_or_printing"),
        ),
        _check(
            "operator_confirms_no_raw_payload_commit",
            True,
            operator_attestation.get("operator_confirms_no_raw_payload_commit"),
        ),
        _check("authority_scope_identity_only", IDENTITY_AUTHORITY_ONLY, frozen_artifact.get("authority_scope")),
        _check(
            "per_ticker_identity_authority_frozen_true",
            True,
            frozen_artifact.get("per_ticker_identity_authority_frozen"),
        ),
        _check("identity_authority_created_true", True, frozen_artifact.get("identity_authority_created")),
        _check("identity_authority_frozen_true", True, frozen_artifact.get("identity_authority_frozen")),
        _check(
            "new_ticker_identity_authority_created_true",
            True,
            frozen_artifact.get("new_ticker_identity_authority_created"),
        ),
        _check("per_ticker_frozen_entries_12", 12, len(entries)),
        _check("per_ticker_freeze_digests_present", True, _per_ticker_freeze_digests_present(entries)),
        _check("unavailable_fields_preserved_as_unavailable", True, all(entry.get("unavailable_fields_preserved_as_unavailable") is True for entry in entries)),
        _check("no_unavailable_fields_fabricated", True, _unavailable_fields_not_fabricated(entries)),
        _check("provider_requests_made_in_freeze_false", False, frozen_artifact.get("provider_requests_made_in_freeze")),
        _check("live_validation_rerun_performed_false", False, frozen_artifact.get("live_validation_rerun_performed")),
        _check("live_provider_transport_enabled_in_freeze_false", False, frozen_artifact.get("live_provider_transport_enabled_in_freeze")),
        _check("corporate_action_authority_created_false", False, frozen_artifact.get("corporate_action_authority_created")),
        _check("split_event_authority_created_false", False, frozen_artifact.get("split_event_authority_created")),
        _check("dividend_event_authority_created_false", False, frozen_artifact.get("dividend_event_authority_created")),
        _check("new_ticker_acquisition_authorized_false", False, frozen_artifact.get("new_ticker_acquisition_authorized")),
        _check("dataset_generation_authorized_false", False, frozen_artifact.get("dataset_generation_authorized")),
        _check("acquisition_generation_authorized_false", False, frozen_artifact.get("acquisition_generation_authorized")),
        _check("canonical_dataset_authorized_false", False, frozen_artifact.get("canonical_dataset_authorized")),
        _check("registry_approval_created_false", False, frozen_artifact.get("registry_approval_created")),
        _check(
            "additional_predictive_evidence_execution_authorized_false",
            False,
            frozen_artifact.get("additional_predictive_evidence_execution_authorized"),
        ),
        _check(
            "additional_predictive_evidence_executed_false",
            False,
            frozen_artifact.get("additional_predictive_evidence_executed"),
        ),
        _check("predictive_experiment_rerun_authorized_false", False, frozen_artifact.get("predictive_experiment_rerun_authorized")),
        _check("predictive_experiment_rerun_performed_false", False, frozen_artifact.get("predictive_experiment_rerun_performed")),
        _check("walk_forward_rerun_performed_false", False, frozen_artifact.get("walk_forward_rerun_performed")),
        _check("label_regeneration_performed_false", False, frozen_artifact.get("label_regeneration_performed")),
        _check("feature_matrix_regeneration_performed_false", False, frozen_artifact.get("feature_matrix_regeneration_performed")),
        _check("new_strategy_scoring_performed_false", False, frozen_artifact.get("new_strategy_scoring_performed")),
        _check("trade_recommendations_generated_false", False, frozen_artifact.get("trade_recommendations_generated")),
        _check("predictive_usefulness_not_accepted", acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED, frozen_artifact.get("predictive_usefulness")),
        _check("predictive_usefulness_acceptance_ready_false", False, frozen_artifact.get("predictive_usefulness_acceptance_ready")),
        _check("predictive_usefulness_acceptance_recommended_false", False, frozen_artifact.get("predictive_usefulness_acceptance_recommended")),
        _check("predictive_usefulness_acceptance_candidate_created_false", False, frozen_artifact.get("predictive_usefulness_acceptance_candidate_created")),
        _check("profitability_not_accepted", acquisition.PROFITABILITY_NOT_ACCEPTED, frozen_artifact.get("profitability")),
        _check("profitability_acceptance_ready_false", False, frozen_artifact.get("profitability_acceptance_ready")),
        _check("profitability_acceptance_recommended_false", False, frozen_artifact.get("profitability_acceptance_recommended")),
        _check("runtime_migration_recommended_false", False, frozen_artifact.get("runtime_migration_recommended")),
        _check("runtime_migration_approved_false", False, frozen_artifact.get("runtime_migration_approved")),
        _check("runtime_migration_active_false", False, frozen_artifact.get("runtime_migration_active")),
        _check("strategy_runtime_migration_false", False, frozen_artifact.get("strategy_runtime_migration")),
        _check("runtime_use_not_authorized", candidate_service.plan_review.plan.NOT_AUTHORIZED, frozen_artifact.get("runtime_use")),
        _check("strategy_use_not_authorized", candidate_service.plan_review.plan.NOT_AUTHORIZED, frozen_artifact.get("strategy_use")),
        _check("paper_trading_not_authorized", candidate_service.plan_review.plan.NOT_AUTHORIZED, frozen_artifact.get("paper_trading")),
        _check("broker_execution_not_authorized", candidate_service.plan_review.plan.NOT_AUTHORIZED, frozen_artifact.get("broker_execution")),
        _check("automatic_stitching_false", False, frozen_artifact.get("automatic_stitching")),
        _check("no_corporate_action_authority_artifact_created", False, frozen_artifact.get("corporate_action_authority_artifact_created")),
        _check("no_acquisition_authorization_created", False, frozen_artifact.get("acquisition_authorization_created")),
        _check("no_dataset_generation_authorization_created", False, frozen_artifact.get("dataset_generation_authorization_created")),
        _check("no_predictive_usefulness_acceptance_artifact_created", False, frozen_artifact.get("predictive_usefulness_acceptance_artifact_created")),
        _check("no_profitability_acceptance_created", False, frozen_artifact.get("profitability_acceptance_created")),
        _check("no_runtime_migration_approval_created", False, frozen_artifact.get("runtime_migration_approval_created")),
    ]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [item for item in checklist if item.get("status") != PASS]
    blockers = [item for item in failed if item.get("severity") == BLOCKER]
    return {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": len(blockers),
        "identity_authority_frozen_by_operator": not failed,
        "authority_scope": IDENTITY_AUTHORITY_ONLY,
        "ready_for_post_identity_freeze_registry_inventory": not failed,
        "ready_for_corporate_action_authority_candidate": False,
        "acquisition_authorized": False,
        "dataset_generation_authorized": False,
        "additional_predictive_evidence_execution_authorized": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def _digest_payload(frozen_artifact: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(frozen_artifact)
    payload.pop("expanded_universe_per_ticker_identity_authority_freeze_digest", None)
    return payload


def expanded_universe_per_ticker_identity_authority_freeze_digest_v1(
    frozen_artifact: dict[str, Any],
) -> str:
    """Return the deterministic semantic digest for the frozen identity artifact."""
    return semantic_digest(_digest_payload(frozen_artifact))


def _base_frozen_artifact(
    review_package: dict[str, Any],
    operator_attestation: dict[str, Any],
) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_FROZEN,
        "schema_version": SCHEMA_VERSION_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_FREEZE_V1,
        "freeze_status": EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_FROZEN,
        "authority_scope": IDENTITY_AUTHORITY_ONLY,
        "created_offline": True,
        "provider_requests_made_in_freeze": False,
        "live_validation_rerun_performed": False,
        "live_provider_transport_enabled_in_freeze": False,
        "source_output_file_reinspection_performed": False,
        "per_ticker_identity_authority_candidate_created": True,
        "per_ticker_identity_authority_review_created": True,
        "per_ticker_identity_authority_frozen": True,
        "identity_authority_created": True,
        "identity_authority_frozen": True,
        "new_ticker_identity_authority_created": True,
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
        "runtime_use": candidate_service.plan_review.plan.NOT_AUTHORIZED,
        "strategy_use": candidate_service.plan_review.plan.NOT_AUTHORIZED,
        "paper_trading": candidate_service.plan_review.plan.NOT_AUTHORIZED,
        "broker_execution": candidate_service.plan_review.plan.NOT_AUTHORIZED,
        "automatic_stitching": False,
        "acquisition_authorization_created": False,
        "dataset_generation_authorization_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
        "identity_authority_candidate_review_package_digest": review_package[
            "expanded_universe_per_ticker_identity_authority_candidate_review_package_digest"
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
        "review_blocker_count": review_package["review_summary"]["blocker_count"],
        "target_universe": list(review_package["target_universe"]),
        "reviewed_universe": list(review_package["validated_universe"]),
        "target_universe_count": review_package["target_universe_count"],
        "identity_fields_to_bind": list(review_package["identity_fields_to_bind"]),
        "identity_evidence_limitations": list(review_package["identity_evidence_limitations"]),
        "per_ticker_frozen_identity_entries": _frozen_entries(review_package),
        "remaining_required_tasks": list(REMAINING_REQUIRED_TASKS),
        "operator_attestation": deepcopy(operator_attestation),
    }


def build_expanded_universe_per_ticker_identity_authority_frozen_v1(
    *,
    operator_attestation: dict[str, Any],
    identity_candidate_review_package: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build and validate the offline identity-only frozen authority artifact."""
    review_package = (
        review_service.build_expanded_universe_per_ticker_identity_authority_candidate_review_package_v1()
        if identity_candidate_review_package is None
        else deepcopy(identity_candidate_review_package)
    )
    review_service.validate_expanded_universe_per_ticker_identity_authority_candidate_review_package_v1(
        review_package
    )
    _validate_operator_attestation(operator_attestation, review_package)
    frozen_artifact = _base_frozen_artifact(review_package, operator_attestation)
    checklist = _checklist(frozen_artifact)
    frozen_artifact["freeze_checklist"] = checklist
    frozen_artifact["freeze_summary"] = _summary(checklist)
    frozen_artifact["expanded_universe_per_ticker_identity_authority_freeze_digest"] = (
        expanded_universe_per_ticker_identity_authority_freeze_digest_v1(frozen_artifact)
    )
    validate_expanded_universe_per_ticker_identity_authority_frozen_v1(frozen_artifact)
    return frozen_artifact


def _reject_forbidden_values(mapping: dict[str, Any], *, path: str = "frozen_artifact") -> None:
    forbidden_true_fields = {
        "provider_requests_made_in_freeze",
        "live_validation_rerun_performed",
        "live_provider_transport_enabled_in_freeze",
        "source_output_file_reinspection_performed",
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
        if key == "artifact_kind" and path != "frozen_artifact":
            raise ExpandedUniversePerTickerIdentityAuthorityFreezeError(
                f"{current_path} must not create another artifact kind"
            )
        if key in forbidden_true_fields and value is True:
            raise ExpandedUniversePerTickerIdentityAuthorityFreezeError(
                f"{current_path} must be false"
            )
        if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"}:
            if value == "AUTHORIZED":
                raise ExpandedUniversePerTickerIdentityAuthorityFreezeError(
                    f"{current_path} must not be AUTHORIZED"
                )
        if key in {"predictive_usefulness", "profitability"} and value == "accepted":
            raise ExpandedUniversePerTickerIdentityAuthorityFreezeError(
                f"{current_path} must not be accepted"
            )
        if isinstance(value, dict):
            _reject_forbidden_values(value, path=current_path)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, dict):
                    _reject_forbidden_values(item, path=f"{current_path}[{index}]")


def _validate_frozen_entries(frozen_artifact: dict[str, Any]) -> None:
    entries = _freeze_entries_from_artifact(frozen_artifact)
    if len(entries) != 12:
        raise ExpandedUniversePerTickerIdentityAuthorityFreezeError(
            "per_ticker_frozen_identity_entries mismatch"
        )
    _expect(
        [entry.get("ticker") for entry in entries],
        VALIDATION_TARGET_UNIVERSE,
        "per_ticker_frozen_identity_entries tickers",
    )
    if not _identity_fields_have_value_status(entries):
        raise ExpandedUniversePerTickerIdentityAuthorityFreezeError(
            "frozen identity fields must use value/status structure"
        )
    if not _unavailable_fields_not_fabricated(entries):
        raise ExpandedUniversePerTickerIdentityAuthorityFreezeError(
            "unavailable frozen identity fields must not be fabricated"
        )
    for entry in entries:
        ticker = entry.get("ticker")
        _expect(
            entry.get("live_validation_status"),
            candidate_service.plan_review.plan.VALIDATED_READ_ONLY,
            f"{ticker}.live_validation_status",
        )
        _expect(
            entry.get("identity_candidate_status"),
            candidate_service.IDENTITY_CANDIDATE_READY_FOR_OPERATOR_REVIEW,
            f"{ticker}.identity_candidate_status",
        )
        _expect(entry.get("identity_review_status"), review_service.REVIEW_PACKAGE_CREATED, f"{ticker}.identity_review_status")
        _expect(entry.get("identity_freeze_status"), IDENTITY_FREEZE_STATUS_FROZEN, f"{ticker}.identity_freeze_status")
        _expect(entry.get("identity_authority_scope"), IDENTITY_AUTHORITY_ONLY, f"{ticker}.identity_authority_scope")
        _expect_true(entry.get("identity_authority_created"), f"{ticker}.identity_authority_created")
        _expect_true(entry.get("identity_authority_frozen"), f"{ticker}.identity_authority_frozen")
        _expect_false(entry.get("corporate_action_authority_created"), f"{ticker}.corporate_action_authority_created")
        _expect_false(entry.get("acquisition_authority_created"), f"{ticker}.acquisition_authority_created")
        _expect_false(entry.get("dataset_generation_authorized"), f"{ticker}.dataset_generation_authorized")
        for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
            _expect(entry.get(field), candidate_service.plan_review.plan.NOT_AUTHORIZED, f"{ticker}.{field}")
        digest = entry.get("per_ticker_identity_freeze_digest")
        if not isinstance(digest, str) or len(digest) != 64:
            raise ExpandedUniversePerTickerIdentityAuthorityFreezeError(
                "per_ticker_identity_freeze_digest missing"
            )
        _expect(digest, per_ticker_identity_freeze_digest_v1(entry), f"{ticker}.per_ticker_identity_freeze_digest")


def validate_expanded_universe_per_ticker_identity_authority_frozen_v1(
    frozen_artifact: dict[str, Any],
) -> dict[str, Any]:
    """Validate the identity-only frozen authority artifact and downstream boundaries."""
    if not isinstance(frozen_artifact, dict):
        raise ExpandedUniversePerTickerIdentityAuthorityFreezeError(
            "frozen_artifact must be a JSON object"
        )
    _reject_forbidden_values(frozen_artifact)
    _expect(
        frozen_artifact.get("artifact_kind"),
        ARTIFACT_KIND_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_FROZEN,
        "artifact_kind",
    )
    _expect(
        frozen_artifact.get("schema_version"),
        SCHEMA_VERSION_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_FREEZE_V1,
        "schema_version",
    )
    _expect(
        frozen_artifact.get("freeze_status"),
        EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_FROZEN,
        "freeze_status",
    )
    for field in (
        "created_offline",
        "per_ticker_identity_authority_candidate_created",
        "per_ticker_identity_authority_review_created",
        "per_ticker_identity_authority_frozen",
        "identity_authority_created",
        "identity_authority_frozen",
        "new_ticker_identity_authority_created",
        "research_only",
    ):
        _expect_true(frozen_artifact.get(field), field)
    for field in (
        "provider_requests_made_in_freeze",
        "live_validation_rerun_performed",
        "live_provider_transport_enabled_in_freeze",
        "source_output_file_reinspection_performed",
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
        _expect_false(frozen_artifact.get(field), field)
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(frozen_artifact.get(field), candidate_service.plan_review.plan.NOT_AUTHORIZED, field)
    for field, expected in {
        "authority_scope": IDENTITY_AUTHORITY_ONLY,
        "identity_authority_candidate_review_package_digest": (
            EXPECTED_IDENTITY_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "identity_authority_candidate_digest": EXPECTED_IDENTITY_AUTHORITY_CANDIDATE_DIGEST,
        "identity_authority_plan_candidate_review_package_digest": (
            EXPECTED_IDENTITY_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "identity_authority_plan_candidate_digest": (
            EXPECTED_IDENTITY_AUTHORITY_PLAN_CANDIDATE_DIGEST
        ),
        "live_ticker_validation_results_review_package_digest": (
            EXPECTED_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_DIGEST
        ),
        "live_ticker_validation_execution_digest": (
            EXPECTED_LIVE_TICKER_VALIDATION_EXECUTION_DIGEST
        ),
        "live_ticker_validation_approval_digest": (
            EXPECTED_LIVE_TICKER_VALIDATION_APPROVAL_DIGEST
        ),
        "ticker_universe_selection_approval_digest": (
            EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST
        ),
        "review_blocker_count": 0,
        "target_universe": VALIDATION_TARGET_UNIVERSE,
        "reviewed_universe": VALIDATION_TARGET_UNIVERSE,
        "target_universe_count": 12,
        "identity_fields_to_bind": IDENTITY_FIELDS_TO_BIND,
        "identity_evidence_limitations": IDENTITY_EVIDENCE_LIMITATIONS,
        "remaining_required_tasks": REMAINING_REQUIRED_TASKS,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
    }.items():
        _expect(frozen_artifact.get(field), expected, field)
    if frozen_artifact.get("target_universe") != frozen_artifact.get("reviewed_universe"):
        raise ExpandedUniversePerTickerIdentityAuthorityFreezeError(
            "target universe differs from reviewed universe"
        )
    _validate_operator_attestation(
        frozen_artifact.get("operator_attestation", {}),
        {
            "expanded_universe_per_ticker_identity_authority_candidate_review_package_digest": frozen_artifact[
                "identity_authority_candidate_review_package_digest"
            ],
            "identity_authority_candidate_digest": frozen_artifact[
                "identity_authority_candidate_digest"
            ],
            "identity_authority_plan_candidate_review_package_digest": frozen_artifact[
                "identity_authority_plan_candidate_review_package_digest"
            ],
            "live_ticker_validation_results_review_package_digest": frozen_artifact[
                "live_ticker_validation_results_review_package_digest"
            ],
        },
    )
    _validate_frozen_entries(frozen_artifact)
    checklist = frozen_artifact.get("freeze_checklist")
    if not isinstance(checklist, list):
        raise ExpandedUniversePerTickerIdentityAuthorityFreezeError("freeze_checklist missing")
    _expect(
        [item.get("check_id") for item in checklist if isinstance(item, dict)],
        REQUIRED_CHECK_IDS,
        "freeze_checklist check IDs",
    )
    expected_checklist = _checklist(frozen_artifact)
    failed = [item for item in expected_checklist if item["status"] != PASS]
    if failed:
        raise ExpandedUniversePerTickerIdentityAuthorityFreezeError(
            f"freeze checklist contains failed check: {failed[0]['check_id']}"
        )
    _expect(checklist, expected_checklist, "freeze_checklist")
    _expect(frozen_artifact.get("freeze_summary"), _summary(expected_checklist), "freeze_summary")
    digest = frozen_artifact.get("expanded_universe_per_ticker_identity_authority_freeze_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise ExpandedUniversePerTickerIdentityAuthorityFreezeError(
            "expanded_universe_per_ticker_identity_authority_freeze_digest missing"
        )
    _expect(
        digest,
        expanded_universe_per_ticker_identity_authority_freeze_digest_v1(frozen_artifact),
        "expanded_universe_per_ticker_identity_authority_freeze_digest",
    )
    return {
        "status": "EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_FROZEN_VALID",
        "artifact_kind": frozen_artifact["artifact_kind"],
        "freeze_status": frozen_artifact["freeze_status"],
        "authority_scope": frozen_artifact["authority_scope"],
        "expanded_universe_per_ticker_identity_authority_freeze_digest": digest,
        "identity_authority_candidate_review_package_digest": frozen_artifact[
            "identity_authority_candidate_review_package_digest"
        ],
        "identity_authority_candidate_digest": frozen_artifact[
            "identity_authority_candidate_digest"
        ],
        "target_universe_count": frozen_artifact["target_universe_count"],
        "per_ticker_frozen_identity_entry_count": len(
            _freeze_entries_from_artifact(frozen_artifact)
        ),
        "total_checks": frozen_artifact["freeze_summary"]["total_checks"],
        "passed_checks": frozen_artifact["freeze_summary"]["passed_checks"],
        "failed_checks": frozen_artifact["freeze_summary"]["failed_checks"],
        "blocker_count": frozen_artifact["freeze_summary"]["blocker_count"],
        "identity_authority_frozen_by_operator": frozen_artifact["freeze_summary"][
            "identity_authority_frozen_by_operator"
        ],
        "ready_for_post_identity_freeze_registry_inventory": frozen_artifact[
            "freeze_summary"
        ]["ready_for_post_identity_freeze_registry_inventory"],
        "ready_for_corporate_action_authority_candidate": False,
        "acquisition_authorized": False,
        "dataset_generation_authorized": False,
        "additional_predictive_evidence_execution_authorized": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def build_expanded_universe_per_ticker_identity_authority_frozen_markdown_v1(
    frozen_artifact: dict[str, Any],
) -> str:
    """Render a sanitized freeze status document."""
    validation = validate_expanded_universe_per_ticker_identity_authority_frozen_v1(
        frozen_artifact
    )
    summary = frozen_artifact["freeze_summary"]
    unavailable_fields = sorted(
        {
            field_name
            for entry in _freeze_entries_from_artifact(frozen_artifact)
            for field_name, field in entry.get("frozen_identity_fields", {}).items()
            if isinstance(field, dict)
            and field.get("status") == candidate_service.UNAVAILABLE_IN_SOURCE
        }
    )
    lines = [
        "# MarketFlow Expanded Universe Per-Ticker Identity Authority Freeze Status",
        "",
        "## Title",
        "- Expanded Universe Per-Ticker Identity Authority Freeze Ceremony v1.",
        "",
        "## Frozen Expanded Universe Identity Authority",
        f"- Artifact kind: `{frozen_artifact['artifact_kind']}`",
        f"- Freeze status: `{frozen_artifact['freeze_status']}`",
        f"- Authority scope: `{frozen_artifact['authority_scope']}`",
        f"- Freeze digest: `{validation['expanded_universe_per_ticker_identity_authority_freeze_digest']}`",
        "",
        "## Operator Attestation",
        f"- Operator decision: `{frozen_artifact['operator_attestation']['operator_decision']}`",
        f"- Operator reference: `{frozen_artifact['operator_attestation']['operator_reference']}`",
        f"- Operator attestation version: `{frozen_artifact['operator_attestation']['operator_attestation_version']}`",
        "",
        "## Source Identity Candidate Review Package",
        f"- Candidate review package digest: `{frozen_artifact['identity_authority_candidate_review_package_digest']}`",
        f"- Candidate digest: `{frozen_artifact['identity_authority_candidate_digest']}`",
        f"- Plan review digest: `{frozen_artifact['identity_authority_plan_candidate_review_package_digest']}`",
        f"- Live validation results review digest: `{frozen_artifact['live_ticker_validation_results_review_package_digest']}`",
        "",
        "## Target Universe",
        f"- Target universe count: `{frozen_artifact['target_universe_count']}`",
        "- Target universe: " + ", ".join(f"`{ticker}`" for ticker in frozen_artifact["target_universe"]),
        "",
        "## Frozen Per-Ticker Identity Entries",
    ]
    lines.extend(
        f"- `{entry['ticker']}`: freeze `{entry['identity_freeze_status']}`, scope `{entry['identity_authority_scope']}`, digest `{entry['per_ticker_identity_freeze_digest']}`"
        for entry in _freeze_entries_from_artifact(frozen_artifact)
    )
    lines.extend(["", "## Preserved Unavailable Fields and Limitations"])
    lines.extend(f"- `{field}`" for field in unavailable_fields)
    lines.extend(f"- `{item}`" for item in frozen_artifact["identity_evidence_limitations"])
    lines.extend(
        [
            "",
            "## Authority Scope",
            f"- per_ticker_identity_authority_frozen: `{frozen_artifact['per_ticker_identity_authority_frozen']}`",
            f"- identity_authority_created: `{frozen_artifact['identity_authority_created']}`",
            f"- identity_authority_frozen: `{frozen_artifact['identity_authority_frozen']}`",
            f"- new_ticker_identity_authority_created: `{frozen_artifact['new_ticker_identity_authority_created']}`",
            "",
            "## Corporate-Action Boundary",
            f"- corporate_action_authority_created: `{frozen_artifact['corporate_action_authority_created']}`",
            f"- split_event_authority_created: `{frozen_artifact['split_event_authority_created']}`",
            f"- dividend_event_authority_created: `{frozen_artifact['dividend_event_authority_created']}`",
            "",
            "## Acquisition Boundary",
            f"- new_ticker_acquisition_authorized: `{frozen_artifact['new_ticker_acquisition_authorized']}`",
            f"- acquisition_generation_authorized: `{frozen_artifact['acquisition_generation_authorized']}`",
            "",
            "## Dataset Boundary",
            f"- dataset_generation_authorized: `{frozen_artifact['dataset_generation_authorized']}`",
            f"- canonical_dataset_authorized: `{frozen_artifact['canonical_dataset_authorized']}`",
            "",
            "## Predictive/Profitability Boundary",
            f"- additional_predictive_evidence_execution_authorized: `{frozen_artifact['additional_predictive_evidence_execution_authorized']}`",
            f"- additional_predictive_evidence_executed: `{frozen_artifact['additional_predictive_evidence_executed']}`",
            f"- predictive_usefulness: `{frozen_artifact['predictive_usefulness']}`",
            f"- profitability: `{frozen_artifact['profitability']}`",
            "",
            "## Runtime Boundary",
            f"- runtime_migration_approved: `{frozen_artifact['runtime_migration_approved']}`",
            f"- runtime_use: `{frozen_artifact['runtime_use']}`",
            f"- strategy_use: `{frozen_artifact['strategy_use']}`",
            f"- paper_trading: `{frozen_artifact['paper_trading']}`",
            f"- broker_execution: `{frozen_artifact['broker_execution']}`",
            "",
            "## Freeze Checklist Summary",
            f"- Total checks: `{summary['total_checks']}`",
            f"- Passed checks: `{summary['passed_checks']}`",
            f"- Failed checks: `{summary['failed_checks']}`",
            f"- Blocker count: `{summary['blocker_count']}`",
            f"- Identity authority frozen by operator: `{summary['identity_authority_frozen_by_operator']}`",
            f"- Ready for post-identity-freeze registry inventory: `{summary['ready_for_post_identity_freeze_registry_inventory']}`",
            "",
            "## Remaining Required Tasks",
        ]
    )
    lines.extend(f"- `{task}`" for task in frozen_artifact["remaining_required_tasks"])
    lines.extend(
        [
            "",
            "## Guardrails",
            "- No Massive.com / Polygon provider request was made.",
            "- No live ticker validation rerun was performed.",
            "- No live provider transport was enabled in freeze.",
            "- Identity authority is frozen only for `IDENTITY_AUTHORITY_ONLY`.",
            "- No corporate-action, acquisition, dataset, predictive, profitability, runtime, paper-trading, broker, or trade-recommendation authorization was created.",
            "",
        ]
    )
    return "\n".join(lines)


def write_expanded_universe_per_ticker_identity_authority_frozen_v1(
    output_dir: str | Path,
    *,
    operator_attestation: dict[str, Any],
    identity_candidate_review_package: dict[str, Any] | None = None,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write the frozen identity artifact JSON without overwriting output."""
    frozen_artifact = build_expanded_universe_per_ticker_identity_authority_frozen_v1(
        identity_candidate_review_package=identity_candidate_review_package,
        operator_attestation=operator_attestation,
    )
    validation = validate_expanded_universe_per_ticker_identity_authority_frozen_v1(
        frozen_artifact
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "expanded_universe_per_ticker_identity_authority_frozen_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise ExpandedUniversePerTickerIdentityAuthorityFreezeError(
            "expanded universe identity authority freeze filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise ExpandedUniversePerTickerIdentityAuthorityFreezeError(
            "expanded universe identity authority freeze output already exists"
        )
    payload = canonical_json_bytes(frozen_artifact)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": _path_text(path),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
    }
