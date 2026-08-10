"""Offline expanded-universe per-ticker identity authority candidate."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import (
    expanded_universe_per_ticker_identity_authority_plan_candidate_operator_review_service as plan_review,
)


ARTIFACT_KIND_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_CANDIDATE = (
    "EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_CANDIDATE"
)
SCHEMA_VERSION_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_CANDIDATE_V1 = (
    "expanded_universe_per_ticker_identity_authority_candidate_v1"
)
EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_READY_FOR_OPERATOR_REVIEW = (
    "EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_READY_FOR_OPERATOR_REVIEW"
)
EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_BLOCKED_MISSING_VALIDATION_OUTPUTS = (
    "EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_BLOCKED_MISSING_VALIDATION_OUTPUTS"
)

DEFAULT_SOURCE_OUTPUT_ROOT = Path(".marketflow/live_ticker_validation/expanded_universe_v1")
IDENTITY_CANDIDATE_READY_FOR_OPERATOR_REVIEW = "IDENTITY_CANDIDATE_READY_FOR_OPERATOR_REVIEW"
CANDIDATE_ONLY_NOT_AUTHORITY = "CANDIDATE_ONLY_NOT_AUTHORITY"
CANDIDATE_ONLY_NOT_FROZEN = "CANDIDATE_ONLY_NOT_FROZEN"
AVAILABLE_FROM_SOURCE = "AVAILABLE_FROM_SOURCE"
UNAVAILABLE_IN_SOURCE = "UNAVAILABLE_IN_SOURCE"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

EXPECTED_IDENTITY_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    "85094dd59296b9d47c2dc456f1dfff5dd463e34db566d36bbca1852114c7ce61"
)
EXPECTED_IDENTITY_AUTHORITY_PLAN_CANDIDATE_DIGEST = (
    plan_review.EXPECTED_REVIEWED_IDENTITY_AUTHORITY_PLAN_CANDIDATE_DIGEST
)
EXPECTED_SOURCE_OUTPUT_DIGESTS = {
    "live_ticker_validation_run_manifest.json": (
        "615af7ec5f525961ddd2b33e6e1dca92e78fa40f3c8d4944fcd252bc31ba0ce0"
    ),
    "ticker_validation_results.json": (
        "8860ebbd6165cfd95f7a75076c1ee6bf0fee476e5c01354fd40f4b0dfb0c38ec"
    ),
    "provider_request_receipts_sanitized.json": (
        "9644b6754a60a7f7da5e23f0f112b063ab6ae3c656442a320824f0ca602bc8ab"
    ),
    "validation_summary.json": (
        "13d39fa36ed117aa2f138181e91db3f841c8f74ca8016689d89250985b55b3a0"
    ),
    "validation_failure_reason_inventory.json": (
        "ead2b32430f88ca7fccf515d58b7057f39c061273adf2479714169b8ef3c5ceb"
    ),
    "operator_review_summary.json": (
        "3c5a93d0f1fd75105111e6f236e470543498d5a23de0ac723d239e6e00ad691b"
    ),
}

VALIDATION_TARGET_UNIVERSE = list(plan_review.VALIDATION_TARGET_UNIVERSE)
IDENTITY_FIELDS_TO_BIND = [
    "ticker",
    "provider_canonical_ticker",
    "provider_name",
    "security_type",
    "market",
    "locale",
    "primary_exchange",
    "active_status",
    "currency",
    "cik",
    "composite_figi",
    "share_class_figi",
    "source_endpoint",
    "provider_response_digest",
    "sanitized_validation_digest",
]
IDENTITY_FIELD_GROUPS = deepcopy(plan_review.IDENTITY_FIELD_GROUPS)
IDENTITY_EVIDENCE_LIMITATIONS = list(plan_review.IDENTITY_EVIDENCE_LIMITATIONS)
FUTURE_IDENTITY_AUTHORITY_CHAIN = [
    "Per-ticker identity authority candidate operator review package.",
    "Identity evidence discrepancy triage, if required.",
    "Per-ticker identity authority freeze ceremony.",
    "Post-freeze identity registry/read-only discovery.",
    "Corporate-action authority chain only after identity freeze.",
    "Acquisition generation chain only after identity and corporate-action authority.",
    "Canonical dataset chain only after acquisition freeze.",
    "Research registry approval only after canonical dataset freeze.",
]
FUTURE_GATES = [
    "per_ticker_identity_authority_candidate_operator_review",
    "identity_discrepancy_triage_if_needed",
    "per_ticker_identity_authority_freeze_approval",
    "post_identity_freeze_registry_inventory",
    "corporate_action_authority_chain_candidate",
    "acquisition_generation_chain_candidate",
    "canonical_dataset_chain_candidate",
    "research_registry_chain_candidate",
]
RISK_CONTROLS = [
    "no_provider_refresh_without_authority",
    "no_raw_provider_payload_commit",
    "no_api_key_storage_or_printing",
    "no_identity_freeze_without_operator_ceremony",
    "no_corporate_action_authority_without_identity_freeze",
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
    "operator_approval_required_before_identity_freeze",
]

REQUIRED_CHECK_IDS = [
    "identity_plan_review_digest_bound",
    "identity_plan_candidate_digest_bound",
    "live_validation_results_review_digest_bound",
    "live_validation_execution_digest_bound",
    "live_validation_approval_digest_bound",
    "ticker_universe_selection_approval_digest_bound",
    "source_output_digests_verified_or_blocked",
    "target_universe_count_12",
    "target_universe_matches_validated_universe",
    "all_targets_validated_read_only",
    "identity_candidate_scope_candidate_only",
    "per_ticker_identity_candidate_entries_12",
    "per_ticker_identity_candidate_status_ready",
    "per_ticker_identity_authority_created_false",
    "per_ticker_identity_freeze_status_not_frozen",
    "per_ticker_identity_review_status_not_created",
    "identity_fields_to_bind_defined",
    "identity_fields_use_status_value_structure",
    "unavailable_fields_marked_unavailable_not_fabricated",
    "provider_response_digest_bound_or_marked_unavailable",
    "sanitized_validation_digest_bound_or_marked_unavailable",
    "per_ticker_identity_candidate_digests_present",
    "identity_field_classification_defined",
    "identity_evidence_limitations_recorded",
    "future_identity_authority_chain_defined",
    "future_gates_defined",
    "risk_controls_defined",
    "provider_requests_made_false",
    "live_validation_rerun_performed_false",
    "live_provider_transport_enabled_false",
    "per_ticker_identity_authority_review_created_false",
    "per_ticker_identity_authority_frozen_false",
    "identity_authority_created_false",
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
    "no_identity_authority_review_created",
    "no_identity_authority_freeze_created",
    "no_corporate_action_authority_created",
    "no_acquisition_authorization_created",
    "no_dataset_generation_authorization_created",
    "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created",
    "no_runtime_migration_approval_created",
]


class ExpandedUniversePerTickerIdentityAuthorityCandidateError(ValueError):
    """Raised when the expanded-universe identity authority candidate is invalid."""


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
        raise ExpandedUniversePerTickerIdentityAuthorityCandidateError(
            f"{field_name} mismatch"
        )


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise ExpandedUniversePerTickerIdentityAuthorityCandidateError(
            f"{field_name} must be true"
        )


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise ExpandedUniversePerTickerIdentityAuthorityCandidateError(
            f"{field_name} must be false"
        )


def _path_text(path: Path) -> str:
    return str(path).replace("\\", "/")


def _resolve_output_root(output_root: str | Path | None) -> Path:
    return DEFAULT_SOURCE_OUTPUT_ROOT if output_root is None else Path(output_root)


def _load_source_outputs(output_root: Path) -> tuple[dict[str, Any], list[dict[str, Any]], bool]:
    files: dict[str, Any] = {}
    manifest: list[dict[str, Any]] = []
    all_available = True
    for name, expected_digest in EXPECTED_SOURCE_OUTPUT_DIGESTS.items():
        path = output_root / name
        exists = path.exists() and path.is_file()
        digest = sha256_bytes(path.read_bytes()) if exists else None
        verified = exists and digest == expected_digest
        manifest.append(
            {
                "name": name,
                "path": _path_text(path),
                "exists": exists,
                "expected_sha256": expected_digest,
                "actual_sha256": digest,
                "digest_verified": verified,
            }
        )
        if not verified:
            all_available = False
            continue
        with path.open("r", encoding="utf-8") as handle:
            files[name] = json.load(handle)
    return files, manifest, all_available


def _future_identity_authority_chain() -> list[dict[str, Any]]:
    return [
        {
            "step_number": index,
            "authority_step": step,
            "execution_required": False,
            "performed_in_this_task": False,
            "operator_approval_required_before_execution": True,
        }
        for index, step in enumerate(FUTURE_IDENTITY_AUTHORITY_CHAIN, start=1)
    ]


def _field(value: Any, status: str) -> dict[str, Any]:
    if status == UNAVAILABLE_IN_SOURCE:
        value = None
    return {"value": value, "status": status}


def _field_from_source(value: Any) -> dict[str, Any]:
    return (
        _field(value, AVAILABLE_FROM_SOURCE)
        if value not in (None, "")
        else _field(None, UNAVAILABLE_IN_SOURCE)
    )


def _per_ticker_identity_candidate_digest_payload(entry: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(entry)
    payload.pop("per_ticker_identity_candidate_digest", None)
    return payload


def per_ticker_identity_candidate_digest_v1(entry: dict[str, Any]) -> str:
    """Return the deterministic semantic digest for one per-ticker identity candidate."""
    return semantic_digest(_per_ticker_identity_candidate_digest_payload(entry))


def _receipt_by_ticker(files: dict[str, Any]) -> dict[str, dict[str, Any]]:
    receipts = files.get("provider_request_receipts_sanitized.json", {}).get(
        "provider_request_receipts", []
    )
    if not isinstance(receipts, list):
        return {}
    return {
        item.get("ticker"): item
        for item in receipts
        if isinstance(item, dict) and item.get("ticker")
    }


def _result_by_ticker(files: dict[str, Any]) -> dict[str, dict[str, Any]]:
    results = files.get("ticker_validation_results.json", {}).get("results", [])
    if not isinstance(results, list):
        return {}
    return {
        item.get("ticker"): item
        for item in results
        if isinstance(item, dict) and item.get("ticker")
    }


def _identity_fields(ticker: str, result: dict[str, Any], receipt: dict[str, Any]) -> dict[str, Any]:
    return {
        "ticker": _field(ticker, AVAILABLE_FROM_SOURCE),
        "provider_canonical_ticker": _field(None, UNAVAILABLE_IN_SOURCE),
        "provider_name": _field_from_source(receipt.get("provider_name")),
        "security_type": _field(None, UNAVAILABLE_IN_SOURCE),
        "market": _field(None, UNAVAILABLE_IN_SOURCE),
        "locale": _field(None, UNAVAILABLE_IN_SOURCE),
        "primary_exchange": _field(None, UNAVAILABLE_IN_SOURCE),
        "active_status": _field_from_source(result.get("active_status")),
        "currency": _field(None, UNAVAILABLE_IN_SOURCE),
        "cik": _field(None, UNAVAILABLE_IN_SOURCE),
        "composite_figi": _field(None, UNAVAILABLE_IN_SOURCE),
        "share_class_figi": _field(None, UNAVAILABLE_IN_SOURCE),
        "source_endpoint": _field_from_source(result.get("provider_endpoint")),
        "provider_response_digest": _field_from_source(
            result.get("provider_response_digest") or receipt.get("provider_response_digest")
        ),
        "sanitized_validation_digest": _field_from_source(
            result.get("sanitized_validation_digest")
        ),
    }


def _per_ticker_entries(files: dict[str, Any]) -> list[dict[str, Any]]:
    results = _result_by_ticker(files)
    receipts = _receipt_by_ticker(files)
    entries: list[dict[str, Any]] = []
    for ticker in VALIDATION_TARGET_UNIVERSE:
        result = results.get(ticker, {})
        receipt = receipts.get(ticker, {})
        entry = {
            "ticker": ticker,
            "identity_candidate_status": IDENTITY_CANDIDATE_READY_FOR_OPERATOR_REVIEW,
            "live_validation_status": result.get("live_validation_status"),
            "identity_authority_scope": CANDIDATE_ONLY_NOT_FROZEN,
            "identity_authority_created": False,
            "identity_freeze_status": plan_review.plan.NOT_FROZEN,
            "identity_review_status": plan_review.plan.NOT_CREATED,
            "identity_fields": _identity_fields(ticker, result, receipt),
            "identity_evidence_source": plan_review.plan.IDENTITY_EVIDENCE_SOURCE,
            "identity_evidence_limitations": list(IDENTITY_EVIDENCE_LIMITATIONS),
        }
        entry["per_ticker_identity_candidate_digest"] = per_ticker_identity_candidate_digest_v1(
            entry
        )
        entries.append(entry)
    return entries


def _base_candidate(
    *,
    output_root: Path,
    files: dict[str, Any],
    source_manifest: list[dict[str, Any]],
    source_verified: bool,
) -> dict[str, Any]:
    ready = source_verified
    status = (
        EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_READY_FOR_OPERATOR_REVIEW
        if ready
        else EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_BLOCKED_MISSING_VALIDATION_OUTPUTS
    )
    entries = _per_ticker_entries(files) if ready else []
    return {
        "artifact_kind": ARTIFACT_KIND_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_CANDIDATE,
        "schema_version": SCHEMA_VERSION_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_CANDIDATE_V1,
        "candidate_status": status,
        "created_offline": True,
        "provider_requests_made": False,
        "live_validation_rerun_performed": False,
        "live_provider_transport_enabled": False,
        "source_output_root": _path_text(output_root),
        "source_output_file_inspection_performed": ready,
        "source_output_digests_verified": ready,
        "source_output_digest_manifest": deepcopy(source_manifest),
        "identity_authority_candidate_scope": CANDIDATE_ONLY_NOT_AUTHORITY,
        "per_ticker_identity_authority_candidate_created": ready,
        "per_ticker_identity_authority_review_created": False,
        "per_ticker_identity_authority_frozen": False,
        "identity_authority_created": False,
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
        "runtime_use": plan_review.plan.NOT_AUTHORIZED,
        "strategy_use": plan_review.plan.NOT_AUTHORIZED,
        "paper_trading": plan_review.plan.NOT_AUTHORIZED,
        "broker_execution": plan_review.plan.NOT_AUTHORIZED,
        "automatic_stitching": False,
        "operator_review_required": True,
        "identity_freeze_requires_operator_ceremony": True,
        "identity_authority_plan_candidate_review_package_digest": (
            EXPECTED_IDENTITY_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "identity_authority_plan_candidate_digest": (
            EXPECTED_IDENTITY_AUTHORITY_PLAN_CANDIDATE_DIGEST
        ),
        "live_ticker_validation_results_review_package_digest": (
            plan_review.plan.EXPECTED_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_DIGEST
        ),
        "live_ticker_validation_execution_digest": (
            plan_review.plan.EXPECTED_LIVE_TICKER_VALIDATION_EXECUTION_DIGEST
        ),
        "live_ticker_validation_approval_digest": (
            plan_review.plan.EXPECTED_LIVE_TICKER_VALIDATION_APPROVAL_DIGEST
        ),
        "live_ticker_validation_candidate_digest": (
            plan_review.plan.EXPECTED_LIVE_TICKER_VALIDATION_CANDIDATE_DIGEST
        ),
        "live_ticker_validation_candidate_review_package_digest": (
            plan_review.plan.EXPECTED_LIVE_TICKER_VALIDATION_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "ticker_universe_selection_approval_digest": (
            plan_review.plan.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST
        ),
        "ticker_universe_selection_candidate_digest": (
            plan_review.plan.EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_DIGEST
        ),
        "ticker_universe_selection_candidate_review_package_digest": (
            plan_review.plan.EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "target_universe": list(VALIDATION_TARGET_UNIVERSE),
        "validated_universe": list(VALIDATION_TARGET_UNIVERSE),
        "target_universe_count": len(VALIDATION_TARGET_UNIVERSE),
        "all_targets_validated_read_only": ready,
        "validated_read_only_count": 12 if ready else 0,
        "provider_request_count": 12 if ready else 0,
        "successful_provider_response_count": 12 if ready else 0,
        "failed_provider_response_count": 0,
        "validation_supports_future_authority_chain_planning": True,
        "validation_creates_new_ticker_authority": False,
        "validation_creates_acquisition_authority": False,
        "validation_creates_dataset_generation_authority": False,
        "validation_creates_predictive_evidence_authority": False,
        "identity_fields_to_bind": list(IDENTITY_FIELDS_TO_BIND),
        "identity_field_groups": deepcopy(IDENTITY_FIELD_GROUPS),
        "identity_evidence_limitations": list(IDENTITY_EVIDENCE_LIMITATIONS),
        "per_ticker_identity_candidate_entries": entries,
        "future_identity_authority_chain": _future_identity_authority_chain(),
        "future_gates": list(FUTURE_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "identity_authority_review_created": False,
        "identity_authority_freeze_created": False,
        "corporate_action_authority_authorized": False,
        "acquisition_authorized": False,
        "acquisition_authorization_created": False,
        "dataset_generation_authorization_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
    }


def _entries(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    entries = candidate.get("per_ticker_identity_candidate_entries")
    return entries if isinstance(entries, list) else []


def _fields_have_value_status(entries: list[dict[str, Any]]) -> bool:
    for entry in entries:
        fields = entry.get("identity_fields")
        if not isinstance(fields, dict) or set(fields) != set(IDENTITY_FIELDS_TO_BIND):
            return False
        for value in fields.values():
            if not isinstance(value, dict) or set(value) != {"value", "status"}:
                return False
            if value.get("status") not in {AVAILABLE_FROM_SOURCE, UNAVAILABLE_IN_SOURCE}:
                return False
    return True


def _unavailable_fields_not_fabricated(entries: list[dict[str, Any]]) -> bool:
    return all(
        field.get("value") is None
        for entry in entries
        for field in entry.get("identity_fields", {}).values()
        if isinstance(field, dict) and field.get("status") == UNAVAILABLE_IN_SOURCE
    )


def _digest_field_bound_or_unavailable(
    entries: list[dict[str, Any]],
    field_name: str,
) -> bool:
    for entry in entries:
        field = entry.get("identity_fields", {}).get(field_name)
        if not isinstance(field, dict):
            return False
        if field.get("status") == AVAILABLE_FROM_SOURCE and not field.get("value"):
            return False
        if field.get("status") == UNAVAILABLE_IN_SOURCE and field.get("value") is not None:
            return False
    return True


def _checklist(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    ready = (
        candidate.get("candidate_status")
        == EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_READY_FOR_OPERATOR_REVIEW
    )
    entries = _entries(candidate)
    return [
        _check(
            "identity_plan_review_digest_bound",
            EXPECTED_IDENTITY_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST,
            candidate.get("identity_authority_plan_candidate_review_package_digest"),
        ),
        _check(
            "identity_plan_candidate_digest_bound",
            EXPECTED_IDENTITY_AUTHORITY_PLAN_CANDIDATE_DIGEST,
            candidate.get("identity_authority_plan_candidate_digest"),
        ),
        _check(
            "live_validation_results_review_digest_bound",
            plan_review.plan.EXPECTED_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_DIGEST,
            candidate.get("live_ticker_validation_results_review_package_digest"),
        ),
        _check(
            "live_validation_execution_digest_bound",
            plan_review.plan.EXPECTED_LIVE_TICKER_VALIDATION_EXECUTION_DIGEST,
            candidate.get("live_ticker_validation_execution_digest"),
        ),
        _check(
            "live_validation_approval_digest_bound",
            plan_review.plan.EXPECTED_LIVE_TICKER_VALIDATION_APPROVAL_DIGEST,
            candidate.get("live_ticker_validation_approval_digest"),
        ),
        _check(
            "ticker_universe_selection_approval_digest_bound",
            plan_review.plan.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST,
            candidate.get("ticker_universe_selection_approval_digest"),
        ),
        _check(
            "source_output_digests_verified_or_blocked",
            True,
            candidate.get("source_output_digests_verified") is True
            or candidate.get("candidate_status")
            == EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_BLOCKED_MISSING_VALIDATION_OUTPUTS,
        ),
        _check("target_universe_count_12", 12, candidate.get("target_universe_count")),
        _check(
            "target_universe_matches_validated_universe",
            True,
            candidate.get("target_universe") == candidate.get("validated_universe") == VALIDATION_TARGET_UNIVERSE,
        ),
        _check("all_targets_validated_read_only", ready, candidate.get("all_targets_validated_read_only")),
        _check(
            "identity_candidate_scope_candidate_only",
            CANDIDATE_ONLY_NOT_AUTHORITY,
            candidate.get("identity_authority_candidate_scope"),
        ),
        _check("per_ticker_identity_candidate_entries_12", 12 if ready else 0, len(entries)),
        _check(
            "per_ticker_identity_candidate_status_ready",
            ready,
            bool(entries)
            and all(
                entry.get("identity_candidate_status") == IDENTITY_CANDIDATE_READY_FOR_OPERATOR_REVIEW
                for entry in entries
            )
            if ready
            else False,
        ),
        _check(
            "per_ticker_identity_authority_created_false",
            True,
            all(entry.get("identity_authority_created") is False for entry in entries) if ready else False,
        ),
        _check(
            "per_ticker_identity_freeze_status_not_frozen",
            True,
            all(entry.get("identity_freeze_status") == plan_review.plan.NOT_FROZEN for entry in entries)
            if ready
            else False,
        ),
        _check(
            "per_ticker_identity_review_status_not_created",
            True,
            all(entry.get("identity_review_status") == plan_review.plan.NOT_CREATED for entry in entries)
            if ready
            else False,
        ),
        _check("identity_fields_to_bind_defined", IDENTITY_FIELDS_TO_BIND, candidate.get("identity_fields_to_bind")),
        _check(
            "identity_fields_use_status_value_structure",
            ready,
            _fields_have_value_status(entries) if ready else False,
        ),
        _check(
            "unavailable_fields_marked_unavailable_not_fabricated",
            ready,
            _unavailable_fields_not_fabricated(entries) if ready else False,
        ),
        _check(
            "provider_response_digest_bound_or_marked_unavailable",
            ready,
            _digest_field_bound_or_unavailable(entries, "provider_response_digest") if ready else False,
        ),
        _check(
            "sanitized_validation_digest_bound_or_marked_unavailable",
            ready,
            _digest_field_bound_or_unavailable(entries, "sanitized_validation_digest") if ready else False,
        ),
        _check(
            "per_ticker_identity_candidate_digests_present",
            ready,
            all(entry.get("per_ticker_identity_candidate_digest") for entry in entries) if ready else False,
        ),
        _check("identity_field_classification_defined", IDENTITY_FIELD_GROUPS, candidate.get("identity_field_groups")),
        _check(
            "identity_evidence_limitations_recorded",
            IDENTITY_EVIDENCE_LIMITATIONS,
            candidate.get("identity_evidence_limitations"),
        ),
        _check(
            "future_identity_authority_chain_defined",
            _future_identity_authority_chain(),
            candidate.get("future_identity_authority_chain"),
        ),
        _check("future_gates_defined", FUTURE_GATES, candidate.get("future_gates")),
        _check("risk_controls_defined", RISK_CONTROLS, candidate.get("risk_controls")),
        _check("provider_requests_made_false", False, candidate.get("provider_requests_made")),
        _check("live_validation_rerun_performed_false", False, candidate.get("live_validation_rerun_performed")),
        _check("live_provider_transport_enabled_false", False, candidate.get("live_provider_transport_enabled")),
        _check(
            "per_ticker_identity_authority_review_created_false",
            False,
            candidate.get("per_ticker_identity_authority_review_created"),
        ),
        _check(
            "per_ticker_identity_authority_frozen_false",
            False,
            candidate.get("per_ticker_identity_authority_frozen"),
        ),
        _check("identity_authority_created_false", False, candidate.get("identity_authority_created")),
        _check("new_ticker_authority_created_false", False, candidate.get("new_ticker_authority_created")),
        _check("new_ticker_acquisition_authorized_false", False, candidate.get("new_ticker_acquisition_authorized")),
        _check("dataset_generation_authorized_false", False, candidate.get("dataset_generation_authorized")),
        _check("corporate_action_authority_created_false", False, candidate.get("corporate_action_authority_created")),
        _check("split_event_authority_created_false", False, candidate.get("split_event_authority_created")),
        _check("dividend_event_authority_created_false", False, candidate.get("dividend_event_authority_created")),
        _check("acquisition_generation_authorized_false", False, candidate.get("acquisition_generation_authorized")),
        _check("canonical_dataset_authorized_false", False, candidate.get("canonical_dataset_authorized")),
        _check("registry_approval_created_false", False, candidate.get("registry_approval_created")),
        _check(
            "additional_predictive_evidence_execution_authorized_false",
            False,
            candidate.get("additional_predictive_evidence_execution_authorized"),
        ),
        _check(
            "additional_predictive_evidence_executed_false",
            False,
            candidate.get("additional_predictive_evidence_executed"),
        ),
        _check("predictive_experiment_rerun_authorized_false", False, candidate.get("predictive_experiment_rerun_authorized")),
        _check("predictive_experiment_rerun_performed_false", False, candidate.get("predictive_experiment_rerun_performed")),
        _check("walk_forward_rerun_performed_false", False, candidate.get("walk_forward_rerun_performed")),
        _check("label_regeneration_performed_false", False, candidate.get("label_regeneration_performed")),
        _check("feature_matrix_regeneration_performed_false", False, candidate.get("feature_matrix_regeneration_performed")),
        _check("new_strategy_scoring_performed_false", False, candidate.get("new_strategy_scoring_performed")),
        _check("trade_recommendations_generated_false", False, candidate.get("trade_recommendations_generated")),
        _check(
            "predictive_usefulness_not_accepted",
            acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
            candidate.get("predictive_usefulness"),
        ),
        _check("predictive_usefulness_acceptance_ready_false", False, candidate.get("predictive_usefulness_acceptance_ready")),
        _check(
            "predictive_usefulness_acceptance_recommended_false",
            False,
            candidate.get("predictive_usefulness_acceptance_recommended"),
        ),
        _check(
            "predictive_usefulness_acceptance_candidate_created_false",
            False,
            candidate.get("predictive_usefulness_acceptance_candidate_created"),
        ),
        _check("profitability_not_accepted", acquisition.PROFITABILITY_NOT_ACCEPTED, candidate.get("profitability")),
        _check("profitability_acceptance_ready_false", False, candidate.get("profitability_acceptance_ready")),
        _check("profitability_acceptance_recommended_false", False, candidate.get("profitability_acceptance_recommended")),
        _check("runtime_migration_recommended_false", False, candidate.get("runtime_migration_recommended")),
        _check("runtime_migration_approved_false", False, candidate.get("runtime_migration_approved")),
        _check("runtime_migration_active_false", False, candidate.get("runtime_migration_active")),
        _check("strategy_runtime_migration_false", False, candidate.get("strategy_runtime_migration")),
        _check("runtime_use_not_authorized", plan_review.plan.NOT_AUTHORIZED, candidate.get("runtime_use")),
        _check("strategy_use_not_authorized", plan_review.plan.NOT_AUTHORIZED, candidate.get("strategy_use")),
        _check("paper_trading_not_authorized", plan_review.plan.NOT_AUTHORIZED, candidate.get("paper_trading")),
        _check("broker_execution_not_authorized", plan_review.plan.NOT_AUTHORIZED, candidate.get("broker_execution")),
        _check("automatic_stitching_false", False, candidate.get("automatic_stitching")),
        _check("no_identity_authority_review_created", False, candidate.get("identity_authority_review_created")),
        _check("no_identity_authority_freeze_created", False, candidate.get("identity_authority_freeze_created")),
        _check("no_corporate_action_authority_created", False, candidate.get("corporate_action_authority_created")),
        _check("no_acquisition_authorization_created", False, candidate.get("acquisition_authorization_created")),
        _check(
            "no_dataset_generation_authorization_created",
            False,
            candidate.get("dataset_generation_authorization_created"),
        ),
        _check(
            "no_predictive_usefulness_acceptance_artifact_created",
            False,
            candidate.get("predictive_usefulness_acceptance_artifact_created"),
        ),
        _check("no_profitability_acceptance_created", False, candidate.get("profitability_acceptance_created")),
        _check("no_runtime_migration_approval_created", False, candidate.get("runtime_migration_approval_created")),
    ]


def _summary(checklist: list[dict[str, Any]], *, candidate_status: str) -> dict[str, Any]:
    failed = [item for item in checklist if item["status"] != PASS]
    blocker_count = sum(1 for item in failed if item.get("severity") == BLOCKER)
    return {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": blocker_count,
        "ready_for_operator_review": (
            candidate_status
            == EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_READY_FOR_OPERATOR_REVIEW
            and not failed
        ),
        "ready_for_identity_freeze": False,
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


def _digest_payload(candidate: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(candidate)
    payload.pop("expanded_universe_per_ticker_identity_authority_candidate_digest", None)
    return payload


def expanded_universe_per_ticker_identity_authority_candidate_digest_v1(
    candidate: dict[str, Any],
) -> str:
    """Return the deterministic semantic digest for the identity authority candidate."""
    return semantic_digest(_digest_payload(candidate))


def build_expanded_universe_per_ticker_identity_authority_candidate_v1(
    *,
    output_root: str | Path | None = None,
) -> dict[str, Any]:
    """Build the offline identity authority candidate without freezing identity."""
    root = _resolve_output_root(output_root)
    files, source_manifest, source_verified = _load_source_outputs(root)
    candidate = _base_candidate(
        output_root=root,
        files=files,
        source_manifest=source_manifest,
        source_verified=source_verified,
    )
    checklist = _checklist(candidate)
    candidate["candidate_checklist"] = checklist
    candidate["candidate_summary"] = _summary(
        checklist,
        candidate_status=candidate["candidate_status"],
    )
    candidate["expanded_universe_per_ticker_identity_authority_candidate_digest"] = (
        expanded_universe_per_ticker_identity_authority_candidate_digest_v1(candidate)
    )
    validate_expanded_universe_per_ticker_identity_authority_candidate_v1(candidate)
    return candidate


def _reject_forbidden_values(mapping: dict[str, Any], *, path: str = "candidate") -> None:
    forbidden_true_fields = {
        "provider_requests_made",
        "live_validation_rerun_performed",
        "live_provider_transport_enabled",
        "per_ticker_identity_authority_review_created",
        "per_ticker_identity_authority_frozen",
        "identity_authority_created",
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
        "identity_authority_review_created",
        "identity_authority_freeze_created",
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
        if key == "artifact_kind" and path != "candidate":
            raise ExpandedUniversePerTickerIdentityAuthorityCandidateError(
                f"{current_path} must not create another artifact kind"
            )
        if key in forbidden_true_fields and value is True:
            raise ExpandedUniversePerTickerIdentityAuthorityCandidateError(
                f"{current_path} must be false"
            )
        if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"}:
            if value == "AUTHORIZED":
                raise ExpandedUniversePerTickerIdentityAuthorityCandidateError(
                    f"{current_path} must not be AUTHORIZED"
                )
        if key in {"predictive_usefulness", "profitability"} and value == "accepted":
            raise ExpandedUniversePerTickerIdentityAuthorityCandidateError(
                f"{current_path} must not be accepted"
            )
        if isinstance(value, dict):
            _reject_forbidden_values(value, path=current_path)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, dict):
                    _reject_forbidden_values(item, path=f"{current_path}[{index}]")


def _validate_entries(candidate: dict[str, Any], *, ready: bool) -> None:
    entries = candidate.get("per_ticker_identity_candidate_entries")
    if ready:
        if not isinstance(entries, list) or len(entries) != 12:
            raise ExpandedUniversePerTickerIdentityAuthorityCandidateError(
                "per_ticker_identity_candidate_entries mismatch"
            )
    elif entries not in ([], None):
        raise ExpandedUniversePerTickerIdentityAuthorityCandidateError(
            "blocked candidate must not fabricate identity entries"
        )
    entries = _entries(candidate)
    if not ready:
        return
    _expect(
        [entry.get("ticker") for entry in entries],
        VALIDATION_TARGET_UNIVERSE,
        "per_ticker_identity_candidate_entries tickers",
    )
    if not _fields_have_value_status(entries):
        raise ExpandedUniversePerTickerIdentityAuthorityCandidateError(
            "identity fields must use value/status structure"
        )
    if not _unavailable_fields_not_fabricated(entries):
        raise ExpandedUniversePerTickerIdentityAuthorityCandidateError(
            "unavailable identity fields must not be fabricated"
        )
    for entry in entries:
        ticker = entry.get("ticker")
        _expect(
            entry.get("identity_candidate_status"),
            IDENTITY_CANDIDATE_READY_FOR_OPERATOR_REVIEW,
            f"{ticker}.identity_candidate_status",
        )
        _expect(
            entry.get("live_validation_status"),
            plan_review.plan.VALIDATED_READ_ONLY,
            f"{ticker}.live_validation_status",
        )
        _expect(
            entry.get("identity_authority_scope"),
            CANDIDATE_ONLY_NOT_FROZEN,
            f"{ticker}.identity_authority_scope",
        )
        _expect_false(entry.get("identity_authority_created"), f"{ticker}.identity_authority_created")
        _expect(
            entry.get("identity_freeze_status"),
            plan_review.plan.NOT_FROZEN,
            f"{ticker}.identity_freeze_status",
        )
        _expect(
            entry.get("identity_review_status"),
            plan_review.plan.NOT_CREATED,
            f"{ticker}.identity_review_status",
        )
        _expect(
            entry.get("identity_evidence_source"),
            plan_review.plan.IDENTITY_EVIDENCE_SOURCE,
            f"{ticker}.identity_evidence_source",
        )
        _expect(
            entry.get("identity_evidence_limitations"),
            IDENTITY_EVIDENCE_LIMITATIONS,
            f"{ticker}.identity_evidence_limitations",
        )
        digest = entry.get("per_ticker_identity_candidate_digest")
        if not isinstance(digest, str) or len(digest) != 64:
            raise ExpandedUniversePerTickerIdentityAuthorityCandidateError(
                "per_ticker_identity_candidate_digest missing"
            )
        _expect(
            digest,
            per_ticker_identity_candidate_digest_v1(entry),
            f"{ticker}.per_ticker_identity_candidate_digest",
        )


def validate_expanded_universe_per_ticker_identity_authority_candidate_v1(
    candidate: dict[str, Any],
) -> dict[str, Any]:
    """Validate the candidate without creating identity freeze or downstream authority."""
    if not isinstance(candidate, dict):
        raise ExpandedUniversePerTickerIdentityAuthorityCandidateError(
            "candidate must be a JSON object"
        )
    _reject_forbidden_values(candidate)
    _expect(
        candidate.get("artifact_kind"),
        ARTIFACT_KIND_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_CANDIDATE,
        "artifact_kind",
    )
    _expect(
        candidate.get("schema_version"),
        SCHEMA_VERSION_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_CANDIDATE_V1,
        "schema_version",
    )
    status = candidate.get("candidate_status")
    if status not in {
        EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_READY_FOR_OPERATOR_REVIEW,
        EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_BLOCKED_MISSING_VALIDATION_OUTPUTS,
    }:
        raise ExpandedUniversePerTickerIdentityAuthorityCandidateError(
            "candidate_status mismatch"
        )
    ready = status == EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_READY_FOR_OPERATOR_REVIEW
    if ready and candidate.get("source_output_digests_verified") is not True:
        raise ExpandedUniversePerTickerIdentityAuthorityCandidateError(
            "status ready while source outputs are missing"
        )
    for field in (
        "created_offline",
        "research_only",
        "operator_review_required",
        "identity_freeze_requires_operator_ceremony",
    ):
        _expect_true(candidate.get(field), field)
    _expect(candidate.get("source_output_file_inspection_performed"), ready, "source_output_file_inspection_performed")
    _expect(candidate.get("source_output_digests_verified"), ready, "source_output_digests_verified")
    _expect(
        candidate.get("per_ticker_identity_authority_candidate_created"),
        ready,
        "per_ticker_identity_authority_candidate_created",
    )
    for field in (
        "provider_requests_made",
        "live_validation_rerun_performed",
        "live_provider_transport_enabled",
        "per_ticker_identity_authority_review_created",
        "per_ticker_identity_authority_frozen",
        "identity_authority_created",
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
        "identity_authority_review_created",
        "identity_authority_freeze_created",
        "corporate_action_authority_authorized",
        "acquisition_authorized",
        "acquisition_authorization_created",
        "dataset_generation_authorization_created",
        "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_created",
        "runtime_migration_approval_created",
    ):
        _expect_false(candidate.get(field), field)
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(candidate.get(field), plan_review.plan.NOT_AUTHORIZED, field)
    for field, expected in {
        "identity_authority_candidate_scope": CANDIDATE_ONLY_NOT_AUTHORITY,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "identity_authority_plan_candidate_review_package_digest": (
            EXPECTED_IDENTITY_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "identity_authority_plan_candidate_digest": (
            EXPECTED_IDENTITY_AUTHORITY_PLAN_CANDIDATE_DIGEST
        ),
        "live_ticker_validation_results_review_package_digest": (
            plan_review.plan.EXPECTED_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_DIGEST
        ),
        "live_ticker_validation_execution_digest": (
            plan_review.plan.EXPECTED_LIVE_TICKER_VALIDATION_EXECUTION_DIGEST
        ),
        "live_ticker_validation_approval_digest": (
            plan_review.plan.EXPECTED_LIVE_TICKER_VALIDATION_APPROVAL_DIGEST
        ),
        "live_ticker_validation_candidate_digest": (
            plan_review.plan.EXPECTED_LIVE_TICKER_VALIDATION_CANDIDATE_DIGEST
        ),
        "live_ticker_validation_candidate_review_package_digest": (
            plan_review.plan.EXPECTED_LIVE_TICKER_VALIDATION_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "ticker_universe_selection_approval_digest": (
            plan_review.plan.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST
        ),
        "ticker_universe_selection_candidate_digest": (
            plan_review.plan.EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_DIGEST
        ),
        "ticker_universe_selection_candidate_review_package_digest": (
            plan_review.plan.EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "target_universe": VALIDATION_TARGET_UNIVERSE,
        "validated_universe": VALIDATION_TARGET_UNIVERSE,
        "target_universe_count": 12,
        "all_targets_validated_read_only": ready,
        "validated_read_only_count": 12 if ready else 0,
        "provider_request_count": 12 if ready else 0,
        "successful_provider_response_count": 12 if ready else 0,
        "failed_provider_response_count": 0,
        "validation_supports_future_authority_chain_planning": True,
        "validation_creates_new_ticker_authority": False,
        "validation_creates_acquisition_authority": False,
        "validation_creates_dataset_generation_authority": False,
        "validation_creates_predictive_evidence_authority": False,
        "identity_fields_to_bind": IDENTITY_FIELDS_TO_BIND,
        "identity_field_groups": IDENTITY_FIELD_GROUPS,
        "identity_evidence_limitations": IDENTITY_EVIDENCE_LIMITATIONS,
        "future_identity_authority_chain": _future_identity_authority_chain(),
        "future_gates": FUTURE_GATES,
        "risk_controls": RISK_CONTROLS,
    }.items():
        if field in {
            "identity_fields_to_bind",
            "identity_field_groups",
            "identity_evidence_limitations",
            "future_identity_authority_chain",
            "future_gates",
            "risk_controls",
        } and not candidate.get(field):
            raise ExpandedUniversePerTickerIdentityAuthorityCandidateError(
                f"{field} missing"
            )
        _expect(candidate.get(field), expected, field)
    if candidate.get("target_universe") != candidate.get("validated_universe"):
        raise ExpandedUniversePerTickerIdentityAuthorityCandidateError(
            "target universe differs from validated universe"
        )
    manifest = candidate.get("source_output_digest_manifest")
    if not isinstance(manifest, list) or len(manifest) != len(EXPECTED_SOURCE_OUTPUT_DIGESTS):
        raise ExpandedUniversePerTickerIdentityAuthorityCandidateError(
            "source_output_digest_manifest missing"
        )
    if ready and not all(item.get("digest_verified") is True for item in manifest):
        raise ExpandedUniversePerTickerIdentityAuthorityCandidateError(
            "source output digests not verified"
        )
    _validate_entries(candidate, ready=ready)
    checklist = candidate.get("candidate_checklist")
    if not isinstance(checklist, list):
        raise ExpandedUniversePerTickerIdentityAuthorityCandidateError(
            "candidate_checklist missing"
        )
    _expect(
        [item.get("check_id") for item in checklist if isinstance(item, dict)],
        REQUIRED_CHECK_IDS,
        "candidate_checklist check IDs",
    )
    expected_checklist = _checklist(candidate)
    failed = [item for item in expected_checklist if item["status"] != PASS]
    if ready and failed:
        raise ExpandedUniversePerTickerIdentityAuthorityCandidateError(
            f"candidate checklist contains failed check: {failed[0]['check_id']}"
        )
    _expect(checklist, expected_checklist, "candidate_checklist")
    _expect(
        candidate.get("candidate_summary"),
        _summary(expected_checklist, candidate_status=status),
        "candidate_summary",
    )
    digest = candidate.get("expanded_universe_per_ticker_identity_authority_candidate_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise ExpandedUniversePerTickerIdentityAuthorityCandidateError(
            "expanded_universe_per_ticker_identity_authority_candidate_digest missing"
        )
    _expect(
        digest,
        expanded_universe_per_ticker_identity_authority_candidate_digest_v1(candidate),
        "expanded_universe_per_ticker_identity_authority_candidate_digest",
    )
    return {
        "status": "EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_CANDIDATE_VALID",
        "artifact_kind": candidate["artifact_kind"],
        "candidate_status": candidate["candidate_status"],
        "expanded_universe_per_ticker_identity_authority_candidate_digest": digest,
        "identity_authority_plan_candidate_review_package_digest": candidate[
            "identity_authority_plan_candidate_review_package_digest"
        ],
        "live_ticker_validation_results_review_package_digest": candidate[
            "live_ticker_validation_results_review_package_digest"
        ],
        "source_output_file_inspection_performed": candidate[
            "source_output_file_inspection_performed"
        ],
        "source_output_digests_verified": candidate["source_output_digests_verified"],
        "target_universe_count": candidate["target_universe_count"],
        "per_ticker_identity_candidate_entry_count": len(_entries(candidate)),
        "total_checks": candidate["candidate_summary"]["total_checks"],
        "passed_checks": candidate["candidate_summary"]["passed_checks"],
        "failed_checks": candidate["candidate_summary"]["failed_checks"],
        "blocker_count": candidate["candidate_summary"]["blocker_count"],
        "ready_for_operator_review": candidate["candidate_summary"]["ready_for_operator_review"],
        "ready_for_identity_freeze": False,
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


def build_expanded_universe_per_ticker_identity_authority_candidate_markdown_v1(
    candidate: dict[str, Any],
) -> str:
    """Render a sanitized identity authority candidate status document."""
    validation = validate_expanded_universe_per_ticker_identity_authority_candidate_v1(
        candidate
    )
    summary = candidate["candidate_summary"]
    unavailable_fields = sorted(
        {
            field_name
            for entry in _entries(candidate)
            for field_name, field in entry.get("identity_fields", {}).items()
            if isinstance(field, dict) and field.get("status") == UNAVAILABLE_IN_SOURCE
        }
    )
    lines = [
        "# MarketFlow Expanded Universe Per-Ticker Identity Authority Candidate Status",
        "",
        "## Title",
        "- Expanded Universe Per-Ticker Identity Authority Candidate v1.",
        "",
        "## Purpose",
        "- Create a candidate-only identity authority package for operator review.",
        "- This artifact does not freeze identity or authorize corporate-action, acquisition, dataset, predictive, profitability, runtime, paper-trading, broker, or trade-recommendation use.",
        "",
        "## Source Live Ticker Validation Evidence",
        f"- Plan review digest: `{candidate['identity_authority_plan_candidate_review_package_digest']}`",
        f"- Plan candidate digest: `{candidate['identity_authority_plan_candidate_digest']}`",
        f"- Live ticker validation results review package digest: `{candidate['live_ticker_validation_results_review_package_digest']}`",
        f"- Candidate digest: `{validation['expanded_universe_per_ticker_identity_authority_candidate_digest']}`",
        f"- Source output digests verified: `{candidate['source_output_digests_verified']}`",
        "",
        "## Target Universe",
        f"- Target universe count: `{candidate['target_universe_count']}`",
        "- Target universe: " + ", ".join(f"`{ticker}`" for ticker in candidate["target_universe"]),
        "",
        "## Per-Ticker Identity Candidate Summary",
    ]
    lines.extend(
        f"- `{entry['ticker']}`: `{entry['identity_candidate_status']}`, freeze `{entry['identity_freeze_status']}`, digest `{entry['per_ticker_identity_candidate_digest']}`"
        for entry in _entries(candidate)
    )
    lines.extend(["", "## Identity Fields to Bind"])
    lines.extend(f"- `{field}`" for field in candidate["identity_fields_to_bind"])
    lines.extend(["", "## Unavailable Fields and Limitations"])
    lines.extend(f"- `{field}`" for field in unavailable_fields)
    lines.extend(f"- `{item}`" for item in candidate["identity_evidence_limitations"])
    lines.extend(["", "## Future Identity Authority Chain"])
    lines.extend(
        f"- `{step['step_number']}`: {step['authority_step']}"
        for step in candidate["future_identity_authority_chain"]
    )
    lines.extend(["", "## Future Gates"])
    lines.extend(f"- `{gate}`" for gate in candidate["future_gates"])
    lines.extend(["", "## Risk Controls"])
    lines.extend(f"- `{control}`" for control in candidate["risk_controls"])
    lines.extend(
        [
            "",
            "## Authority Boundary",
            f"- identity_authority_candidate_scope: `{candidate['identity_authority_candidate_scope']}`",
            f"- per_ticker_identity_authority_candidate_created: `{candidate['per_ticker_identity_authority_candidate_created']}`",
            f"- per_ticker_identity_authority_review_created: `{candidate['per_ticker_identity_authority_review_created']}`",
            f"- per_ticker_identity_authority_frozen: `{candidate['per_ticker_identity_authority_frozen']}`",
            f"- new_ticker_authority_created: `{candidate['new_ticker_authority_created']}`",
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
            f"- Ready for identity freeze: `{summary['ready_for_identity_freeze']}`",
            "",
            "## Guardrails",
            "- No Massive.com / Polygon provider request was made.",
            "- No live ticker validation rerun was performed.",
            "- No live provider transport was enabled.",
            "- No identity freeze was created.",
            "- No corporate-action, acquisition, dataset, predictive, profitability, runtime, paper-trading, broker, or trade-recommendation authorization was created.",
            "",
        ]
    )
    return "\n".join(lines)


def write_expanded_universe_per_ticker_identity_authority_candidate_v1(
    output_dir: str | Path,
    *,
    output_root: str | Path | None = None,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write the identity authority candidate JSON without overwriting output."""
    candidate = build_expanded_universe_per_ticker_identity_authority_candidate_v1(
        output_root=output_root
    )
    validation = validate_expanded_universe_per_ticker_identity_authority_candidate_v1(
        candidate
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "expanded_universe_per_ticker_identity_authority_candidate_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise ExpandedUniversePerTickerIdentityAuthorityCandidateError(
            "expanded universe identity authority candidate filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise ExpandedUniversePerTickerIdentityAuthorityCandidateError(
            "expanded universe identity authority candidate output already exists"
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
