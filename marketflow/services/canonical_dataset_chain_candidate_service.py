"""Offline canonical-dataset-chain planning candidate for the expanded universe."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_generation_freeze_service as freeze


ARTIFACT_KIND_CANONICAL_DATASET_CHAIN_CANDIDATE = "CANONICAL_DATASET_CHAIN_CANDIDATE"
SCHEMA_VERSION_CANONICAL_DATASET_CHAIN_CANDIDATE_V1 = "canonical_dataset_chain_candidate_v1"
CANONICAL_DATASET_CHAIN_READY_FOR_OPERATOR_REVIEW = "CANONICAL_DATASET_CHAIN_READY_FOR_OPERATOR_REVIEW"
CANONICAL_DATASET_CHAIN_OBJECTIVE = "PLAN_CANONICAL_DATASET_CHAIN_FOR_ACQUISITION_GENERATION_FROZEN_EXPANDED_UNIVERSE"
CANONICAL_DATASET_CHAIN_SCOPE = "CHAIN_CANDIDATE_ONLY_NOT_DATASET_AUTHORIZATION"
CANONICAL_DATASET_MODE = "PLANNED_NOT_GENERATED"
CANONICAL_DATASET_AUTHORITY_STATUS = "NOT_AUTHORIZED"
PLANNED_READY_FOR_OPERATOR_REVIEW = "PLANNED_READY_FOR_OPERATOR_REVIEW"
PLANNED_NOT_GENERATED = "PLANNED_NOT_GENERATED"
RESEARCH_ONLY_NON_ACTIONABLE = "RESEARCH_ONLY_NON_ACTIONABLE"

EXPECTED_ACQUISITION_GENERATION_FREEZE_DIGEST = "534d72f842a44162bf07d32bbd6c2defb4e0064deb148fb92e785a5514319bd5"
EXPECTED_ACQUISITION_GENERATION_APPROVAL_DIGEST = freeze.EXPECTED_ACQUISITION_GENERATION_APPROVAL_DIGEST
EXPECTED_ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST = freeze.EXPECTED_ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST
EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_EXECUTION_DIGEST = freeze.EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_EXECUTION_DIGEST
EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST = freeze.EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST
EXPECTED_ACQUISITION_GENERATION_CHAIN_CANDIDATE_REVIEW_PACKAGE_DIGEST = freeze.EXPECTED_ACQUISITION_GENERATION_CHAIN_CANDIDATE_REVIEW_PACKAGE_DIGEST
EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST = freeze.EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST
EXPECTED_COMBINED_READINESS_REVIEW_PACKAGE_DIGEST = freeze.EXPECTED_COMBINED_READINESS_REVIEW_PACKAGE_DIGEST
EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST = freeze.EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST
EXPECTED_DIVIDEND_EVENT_AUTHORITY_FREEZE_DIGEST = freeze.EXPECTED_DIVIDEND_EVENT_AUTHORITY_FREEZE_DIGEST
EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST = freeze.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST
EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST = freeze.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST
EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST = "c380dd016035289d11b79723daafc6bdec694928233ff464ec386239ea820c82"

TARGET_UNIVERSE = list(freeze.TARGET_UNIVERSE)
PASS = freeze.PASS
FAIL = freeze.FAIL
BLOCKER = freeze.BLOCKER
NOT_AUTHORIZED = freeze.NOT_AUTHORIZED
NOT_ACCEPTED = freeze.NOT_ACCEPTED
PROFITABILITY_NOT_ACCEPTED = freeze.PROFITABILITY_NOT_ACCEPTED
ACQUISITION_EVIDENCE_COLLECTED_READ_ONLY = freeze.ACQUISITION_EVIDENCE_COLLECTED_READ_ONLY

CANONICAL_DATASET_PLANNING_DIMENSIONS = [
    "source_acquisition_generation_freeze_binding",
    "source_corporate_action_authority_binding",
    "source_identity_authority_binding",
    "source_split_dividend_authority_binding",
    "ticker_universe_order_policy",
    "daily_bar_schema_policy",
    "ohlcv_field_policy",
    "timestamp_timezone_policy",
    "trading_calendar_policy",
    "session_filter_policy",
    "adjusted_unadjusted_price_policy",
    "split_adjustment_binding_policy",
    "dividend_adjustment_binding_policy",
    "meta_reduced_bar_count_preservation_policy",
    "missing_bar_gap_policy",
    "data_quality_validation_policy",
    "deterministic_sorting_policy",
    "canonical_column_order_policy",
    "canonical_metadata_policy",
    "digest_manifest_policy",
    "sanitized_output_policy",
    "raw_payload_policy",
]

SOURCE_PROFILE = {
    "date_range_start": "2022-01-01",
    "date_range_end": "2025-12-31",
    "timeframe": "1d",
    "profile": "RTH_FULL_SESSION_1D",
    "source_evidence_scope": "READ_ONLY_HISTORICAL_MARKET_DATA_ACQUISITION_REQUESTS_ONLY",
    "expected_ticker_count": 12,
    "historical_bar_evidence_collected_count": 12,
    "generated_acquisition_output_count": 7,
}

FUTURE_CANONICAL_DATASET_CHAIN = [
    "Canonical dataset chain candidate operator review package.",
    "Canonical dataset approval ceremony if required.",
    "Canonical dataset generation execution.",
    "Canonical dataset results review package.",
    "Canonical dataset freeze ceremony.",
    "Research registry candidate.",
    "Research registry operator review.",
    "Research registry approval ceremony.",
    "Additional predictive evidence planning, if required.",
    "Runtime migration chain, if ever separately authorized.",
]

FUTURE_GATES = [
    "canonical_dataset_chain_candidate_operator_review",
    "canonical_dataset_approval_if_required",
    "canonical_dataset_generation_execution",
    "canonical_dataset_results_review",
    "canonical_dataset_freeze",
    "research_registry_candidate",
    "research_registry_operator_review",
    "research_registry_approval",
    "additional_predictive_evidence_chain_if_required",
    "runtime_migration_chain_if_ever_authorized",
]

RISK_CONTROLS = [
    "no_dataset_generation_without_operator_approval",
    "no_canonical_dataset_freeze_without_results_review",
    "no_registry_approval_without_canonical_dataset_freeze",
    "no_raw_provider_payload_commit",
    "no_api_key_storage_or_printing",
    "preserve_meta_reduced_bar_count",
    "no_missing_bar_fabrication",
    "no_calendar_session_inference_without_review",
    "no_adjustment_policy_change_without_review",
    "no_predictive_label_use_without_registry_approval",
    "no_runtime_source_switch",
    "no_automatic_stitching",
    "no_broker_execution",
    "no_paper_trading",
    "no_trade_recommendations",
    "no_predictive_usefulness_acceptance",
    "no_profitability_acceptance",
    "all_outputs_labeled_research_only",
]

PLANNED_OUTPUT_NAMES = [
    "canonical_dataset_chain_manifest",
    "canonical_dataset_schema_contract_template",
    "per_ticker_canonical_dataset_requirement_matrix",
    "canonical_dataset_generation_plan_template",
    "canonical_data_quality_report_template",
    "canonical_dataset_digest_manifest_template",
    "canonical_dataset_results_review_template",
    "canonical_dataset_freeze_template",
    "research_registry_candidate_template",
    "operator_review_summary_template",
]

REQUIRED_CHECK_IDS = [
    "acquisition_generation_freeze_digest_bound",
    "acquisition_generation_approval_digest_bound",
    "acquisition_evidence_results_review_digest_bound",
    "corporate_action_authority_approval_digest_bound",
    "identity_freeze_digest_bound",
    "target_universe_count_12",
    "target_universe_matches_acquisition_generation_freeze_universe",
    "acquisition_generation_frozen_true",
    "ready_for_canonical_dataset_chain_candidate_true",
    "canonical_dataset_chain_candidate_created_true",
    "canonical_dataset_chain_scope_candidate_only",
    "canonical_dataset_authority_status_not_authorized",
    "per_ticker_canonical_dataset_chain_entries_12",
    "per_ticker_canonical_dataset_chain_digests_present",
    "canonical_dataset_planning_dimensions_defined",
    "source_profile_preserved",
    "meta_reduced_bar_count_preserved",
    "future_canonical_dataset_chain_defined",
    "future_gates_defined",
    "risk_controls_defined",
    "planned_outputs_not_generated",
    "planned_outputs_research_only",
    "provider_requests_made_false",
    "live_provider_transport_enabled_false",
    "market_data_acquisition_performed_false",
    "dataset_generation_performed_false",
    "dataset_generation_authorized_false",
    "canonical_dataset_authorized_false",
    "canonical_dataset_candidate_created_false",
    "canonical_dataset_generation_executed_false",
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
    "no_dataset_generation_artifact_created",
    "no_canonical_dataset_artifact_created",
    "no_registry_approval_created",
    "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created",
    "no_runtime_migration_approval_created",
]


class CanonicalDatasetChainCandidateError(ValueError):
    """Raised when candidate evidence or an authority boundary is invalid."""


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise CanonicalDatasetChainCandidateError(f"{field} mismatch")


def _expect_true(actual: Any, field: str) -> None:
    if actual is not True:
        raise CanonicalDatasetChainCandidateError(f"{field} must be true")


def _expect_false(actual: Any, field: str) -> None:
    if actual is not False:
        raise CanonicalDatasetChainCandidateError(f"{field} must be false")


def _expect_digest(actual: Any, field: str) -> None:
    if not isinstance(actual, str) or len(actual) != 64:
        raise CanonicalDatasetChainCandidateError(f"{field} missing")


def _source_freeze_attestation() -> dict[str, Any]:
    return freeze.build_acquisition_generation_freeze_attestation_v1(
        operator_reference="USER_REQUEST_1BACF9A7",
        operator_attestation_timestamp_utc="2026-08-14T13:30:00Z",
        operator_attestation_phrase=freeze.REQUIRED_ACQUISITION_GENERATION_FREEZE_ATTESTATION_PHRASE,
        operator_confirms_acquisition_generation_approval_digest=EXPECTED_ACQUISITION_GENERATION_APPROVAL_DIGEST,
        operator_confirms_acquisition_evidence_results_review_digest=EXPECTED_ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        operator_confirms_acquisition_provider_evidence_execution_digest=EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        operator_confirms_acquisition_provider_evidence_request_approval_digest=EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST,
        operator_confirms_acquisition_chain_candidate_review_digest=EXPECTED_ACQUISITION_GENERATION_CHAIN_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        operator_confirms_corporate_action_authority_approval_digest=EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST,
        operator_confirms_target_universe=list(TARGET_UNIVERSE),
        operator_confirms_target_count=12,
        operator_confirms_historical_bar_evidence_collected_count=12,
        operator_confirms_provider_request_count=12,
        operator_confirms_successful_provider_response_count=12,
        operator_confirms_failed_provider_response_count_zero=True,
        operator_confirms_meta_reduced_bar_count_preserved=True,
        operator_confirms_freeze_scope_acquisition_generation_only=True,
        operator_confirms_acquisition_generation_authorized=True,
        operator_confirms_acquisition_generation_approved=True,
        operator_confirms_ready_for_canonical_dataset_chain_candidate=True,
        operator_confirms_no_acquisition_generation_execution=True,
        operator_confirms_no_dataset_generation_authorization=True,
        operator_confirms_no_canonical_dataset_authorization=True,
        operator_confirms_no_canonical_dataset_candidate=True,
        operator_confirms_no_canonical_dataset_freeze=True,
        operator_confirms_no_registry_approval=True,
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


def _source_freeze() -> dict[str, Any]:
    artifact = freeze.build_acquisition_generation_frozen_v1(
        operator_attestation=_source_freeze_attestation()
    )
    validation = freeze.validate_acquisition_generation_frozen_v1(artifact)
    _expect(validation.get("acquisition_generation_freeze_digest"), EXPECTED_ACQUISITION_GENERATION_FREEZE_DIGEST, "source freeze digest")
    _expect(validation.get("blocker_count"), 0, "source freeze blocker_count")
    return artifact


def per_ticker_canonical_dataset_chain_candidate_digest_v1(entry: dict[str, Any]) -> str:
    payload = deepcopy(entry)
    payload.pop("per_ticker_canonical_dataset_chain_candidate_digest", None)
    return semantic_digest(payload)


def _per_ticker_entries(source: dict[str, Any]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for row in source["per_ticker_acquisition_generation_freezes"]:
        entry = {
            "ticker": row["ticker"],
            "identity_authority_status": "FROZEN",
            "split_event_authority_status": "FROZEN",
            "dividend_event_authority_status": "FROZEN",
            "corporate_action_authority_status": "APPROVED",
            "acquisition_generation_status": "FROZEN",
            "canonical_dataset_chain_status": PLANNED_READY_FOR_OPERATOR_REVIEW,
            "historical_bar_evidence_status": row["historical_bar_evidence_status"],
            "historical_bar_count": row["historical_bar_count"],
            "meta_reduced_bar_count_flag": row["meta_reduced_bar_count_flag"],
            "dataset_generation_authorized": False,
            "canonical_dataset_authorized": False,
            "canonical_dataset_candidate_created": False,
            "canonical_dataset_generation_executed": False,
            "canonical_dataset_frozen": False,
            "registry_approval_created": False,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
        }
        entry["per_ticker_canonical_dataset_chain_candidate_digest"] = (
            per_ticker_canonical_dataset_chain_candidate_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _planned_outputs() -> list[dict[str, str]]:
    return [
        {
            "output_name": name,
            "generation_status": PLANNED_NOT_GENERATED,
            "classification": RESEARCH_ONLY_NON_ACTIONABLE,
        }
        for name in PLANNED_OUTPUT_NAMES
    ]


def _base_candidate(source: dict[str, Any]) -> dict[str, Any]:
    source_fields = [
        "acquisition_generation_approval_digest",
        "acquisition_evidence_results_review_package_digest",
        "acquisition_provider_evidence_execution_digest",
        "acquisition_provider_evidence_request_approval_digest",
        "acquisition_generation_chain_candidate_review_package_digest",
        "corporate_action_authority_approval_digest",
        "combined_split_dividend_corporate_action_readiness_review_package_digest",
        "split_event_authority_freeze_digest",
        "dividend_event_authority_freeze_digest",
        "identity_authority_freeze_digest",
        "ticker_universe_selection_approval_digest",
        "target_universe",
        "target_universe_count",
        "new_ticker_acquisition_authorized",
        "acquisition_generation_authorized",
        "acquisition_generation_approved",
        "acquisition_generation_frozen",
        "acquisition_generation_executed",
        "acquisition_generation_results_created",
        "corporate_action_authority_created",
        "corporate_action_authority_approved",
        "corporate_action_authority_scope",
        "split_event_authority_created",
        "split_event_authority_frozen",
        "split_event_authority_scope",
        "dividend_event_authority_created",
        "dividend_event_authority_frozen",
        "dividend_event_authority_scope",
        "identity_authority_created",
        "identity_authority_frozen",
    ]
    candidate = {field: deepcopy(source[field]) for field in source_fields}
    candidate.update({
        "artifact_kind": ARTIFACT_KIND_CANONICAL_DATASET_CHAIN_CANDIDATE,
        "schema_version": SCHEMA_VERSION_CANONICAL_DATASET_CHAIN_CANDIDATE_V1,
        "candidate_status": CANONICAL_DATASET_CHAIN_READY_FOR_OPERATOR_REVIEW,
        "created_offline": True,
        "provider_requests_made": False,
        "live_provider_transport_enabled": False,
        "market_data_acquisition_performed": False,
        "dataset_generation_performed": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "canonical_dataset_chain_candidate_created": True,
        "canonical_dataset_chain_ready_for_operator_review": True,
        "canonical_dataset_chain_approved": False,
        "dataset_generation_authorized": False,
        "canonical_dataset_authorized": False,
        "canonical_dataset_candidate_created": False,
        "canonical_dataset_generation_executed": False,
        "canonical_dataset_frozen": False,
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
        "operator_review_required": True,
        "acquisition_generation_freeze_digest": source["acquisition_generation_freeze_digest"],
        "post_identity_freeze_registry_inventory_approval_digest": EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST,
        "source_acquisition_generation_freeze_blocker_count": source["freeze_summary"]["blocker_count"],
        "ready_for_canonical_dataset_chain_candidate": source["ready_for_canonical_dataset_chain_candidate"],
        "canonical_dataset_chain_objective": CANONICAL_DATASET_CHAIN_OBJECTIVE,
        "canonical_dataset_chain_scope": CANONICAL_DATASET_CHAIN_SCOPE,
        "canonical_dataset_mode": CANONICAL_DATASET_MODE,
        "canonical_dataset_authority_status": CANONICAL_DATASET_AUTHORITY_STATUS,
        "canonical_dataset_planning_dimensions": list(CANONICAL_DATASET_PLANNING_DIMENSIONS),
        "canonical_dataset_source_profile": deepcopy(SOURCE_PROFILE),
        "per_ticker_canonical_dataset_chain_candidates": _per_ticker_entries(source),
        "meta_reduced_bar_count_preserved": source["meta_reduced_bar_count_preserved"],
        "future_canonical_dataset_chain": list(FUTURE_CANONICAL_DATASET_CHAIN),
        "future_gates": list(FUTURE_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "planned_outputs": _planned_outputs(),
        "dataset_generation_artifact_created": False,
        "canonical_dataset_artifact_created": False,
        "registry_approval_artifact_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
    })
    return candidate


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


def _checklist(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    entries = candidate["per_ticker_canonical_dataset_chain_candidates"]
    outputs = candidate["planned_outputs"]
    values: dict[str, tuple[Any, Any]] = {
        "acquisition_generation_freeze_digest_bound": (EXPECTED_ACQUISITION_GENERATION_FREEZE_DIGEST, candidate.get("acquisition_generation_freeze_digest")),
        "acquisition_generation_approval_digest_bound": (EXPECTED_ACQUISITION_GENERATION_APPROVAL_DIGEST, candidate.get("acquisition_generation_approval_digest")),
        "acquisition_evidence_results_review_digest_bound": (EXPECTED_ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST, candidate.get("acquisition_evidence_results_review_package_digest")),
        "corporate_action_authority_approval_digest_bound": (EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST, candidate.get("corporate_action_authority_approval_digest")),
        "identity_freeze_digest_bound": (EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST, candidate.get("identity_authority_freeze_digest")),
        "target_universe_count_12": (12, candidate.get("target_universe_count")),
        "target_universe_matches_acquisition_generation_freeze_universe": (TARGET_UNIVERSE, candidate.get("target_universe")),
        "acquisition_generation_frozen_true": (True, candidate.get("acquisition_generation_frozen")),
        "ready_for_canonical_dataset_chain_candidate_true": (True, candidate.get("ready_for_canonical_dataset_chain_candidate")),
        "canonical_dataset_chain_candidate_created_true": (True, candidate.get("canonical_dataset_chain_candidate_created")),
        "canonical_dataset_chain_scope_candidate_only": (CANONICAL_DATASET_CHAIN_SCOPE, candidate.get("canonical_dataset_chain_scope")),
        "canonical_dataset_authority_status_not_authorized": (CANONICAL_DATASET_AUTHORITY_STATUS, candidate.get("canonical_dataset_authority_status")),
        "per_ticker_canonical_dataset_chain_entries_12": (12, len(entries)),
        "per_ticker_canonical_dataset_chain_digests_present": (True, bool(entries) and all(isinstance(row.get("per_ticker_canonical_dataset_chain_candidate_digest"), str) and len(row["per_ticker_canonical_dataset_chain_candidate_digest"]) == 64 for row in entries)),
        "canonical_dataset_planning_dimensions_defined": (CANONICAL_DATASET_PLANNING_DIMENSIONS, candidate.get("canonical_dataset_planning_dimensions")),
        "source_profile_preserved": (SOURCE_PROFILE, candidate.get("canonical_dataset_source_profile")),
        "meta_reduced_bar_count_preserved": (True, candidate.get("meta_reduced_bar_count_preserved")),
        "future_canonical_dataset_chain_defined": (FUTURE_CANONICAL_DATASET_CHAIN, candidate.get("future_canonical_dataset_chain")),
        "future_gates_defined": (FUTURE_GATES, candidate.get("future_gates")),
        "risk_controls_defined": (RISK_CONTROLS, candidate.get("risk_controls")),
        "planned_outputs_not_generated": (True, bool(outputs) and all(row.get("generation_status") == PLANNED_NOT_GENERATED for row in outputs)),
        "planned_outputs_research_only": (True, bool(outputs) and all(row.get("classification") == RESEARCH_ONLY_NON_ACTIONABLE for row in outputs)),
        "predictive_usefulness_not_accepted": (NOT_ACCEPTED, candidate.get("predictive_usefulness")),
        "profitability_not_accepted": (PROFITABILITY_NOT_ACCEPTED, candidate.get("profitability")),
        "runtime_use_not_authorized": (NOT_AUTHORIZED, candidate.get("runtime_use")),
        "strategy_use_not_authorized": (NOT_AUTHORIZED, candidate.get("strategy_use")),
        "paper_trading_not_authorized": (NOT_AUTHORIZED, candidate.get("paper_trading")),
        "broker_execution_not_authorized": (NOT_AUTHORIZED, candidate.get("broker_execution")),
    }
    false_checks = {
        "provider_requests_made_false": "provider_requests_made",
        "live_provider_transport_enabled_false": "live_provider_transport_enabled",
        "market_data_acquisition_performed_false": "market_data_acquisition_performed",
        "dataset_generation_performed_false": "dataset_generation_performed",
        "dataset_generation_authorized_false": "dataset_generation_authorized",
        "canonical_dataset_authorized_false": "canonical_dataset_authorized",
        "canonical_dataset_candidate_created_false": "canonical_dataset_candidate_created",
        "canonical_dataset_generation_executed_false": "canonical_dataset_generation_executed",
        "canonical_dataset_frozen_false": "canonical_dataset_frozen",
        "registry_approval_created_false": "registry_approval_created",
        "additional_predictive_evidence_execution_authorized_false": "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed_false": "additional_predictive_evidence_executed",
        "predictive_experiment_rerun_authorized_false": "predictive_experiment_rerun_authorized",
        "new_strategy_scoring_performed_false": "new_strategy_scoring_performed",
        "trade_recommendations_generated_false": "trade_recommendations_generated",
        "runtime_migration_approved_false": "runtime_migration_approved",
        "automatic_stitching_false": "automatic_stitching",
        "no_dataset_generation_artifact_created": "dataset_generation_artifact_created",
        "no_canonical_dataset_artifact_created": "canonical_dataset_artifact_created",
        "no_registry_approval_created": "registry_approval_artifact_created",
        "no_predictive_usefulness_acceptance_artifact_created": "predictive_usefulness_acceptance_artifact_created",
        "no_profitability_acceptance_created": "profitability_acceptance_created",
        "no_runtime_migration_approval_created": "runtime_migration_approval_created",
    }
    values.update({check_id: (False, candidate.get(field)) for check_id, field in false_checks.items()})
    return [_check(check_id, *values[check_id]) for check_id in REQUIRED_CHECK_IDS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [row for row in checklist if row["status"] != PASS]
    return {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row["severity"] == BLOCKER for row in failed),
        "ready_for_operator_review": not failed,
        "ready_for_canonical_dataset_approval": False,
        "ready_for_canonical_dataset_generation_execution": False,
        "ready_for_canonical_dataset_freeze": False,
        "ready_for_research_registry_candidate": False,
        "dataset_generation_authorized": False,
        "canonical_dataset_authorized": False,
        "canonical_dataset_candidate_created": False,
        "canonical_dataset_frozen": False,
        "registry_approval_created": False,
        "additional_predictive_evidence_execution_authorized": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def canonical_dataset_chain_candidate_digest_v1(candidate: dict[str, Any]) -> str:
    payload = deepcopy(candidate)
    payload.pop("canonical_dataset_chain_candidate_digest", None)
    return semantic_digest(payload)


def build_canonical_dataset_chain_candidate_v1() -> dict[str, Any]:
    """Build a deterministic planning candidate without provider or dataset work."""
    candidate = _base_candidate(_source_freeze())
    candidate["candidate_checklist"] = _checklist(candidate)
    candidate["candidate_summary"] = _summary(candidate["candidate_checklist"])
    candidate["canonical_dataset_chain_candidate_digest"] = canonical_dataset_chain_candidate_digest_v1(candidate)
    validate_canonical_dataset_chain_candidate_v1(candidate)
    return candidate


def _validate_per_ticker(candidate: dict[str, Any]) -> None:
    entries = candidate.get("per_ticker_canonical_dataset_chain_candidates")
    if not isinstance(entries, list) or len(entries) != 12:
        raise CanonicalDatasetChainCandidateError("per_ticker candidates mismatch")
    _expect([row.get("ticker") for row in entries], TARGET_UNIVERSE, "per_ticker tickers")
    for row in entries:
        ticker = row["ticker"]
        expected = {
            "identity_authority_status": "FROZEN",
            "split_event_authority_status": "FROZEN",
            "dividend_event_authority_status": "FROZEN",
            "corporate_action_authority_status": "APPROVED",
            "acquisition_generation_status": "FROZEN",
            "canonical_dataset_chain_status": PLANNED_READY_FOR_OPERATOR_REVIEW,
            "historical_bar_evidence_status": ACQUISITION_EVIDENCE_COLLECTED_READ_ONLY,
            "historical_bar_count": 913 if ticker == "META" else 1003,
            "meta_reduced_bar_count_flag": ticker == "META",
            "dataset_generation_authorized": False,
            "canonical_dataset_authorized": False,
            "canonical_dataset_candidate_created": False,
            "canonical_dataset_generation_executed": False,
            "canonical_dataset_frozen": False,
            "registry_approval_created": False,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
        }
        for field, value in expected.items():
            _expect(row.get(field), value, f"{ticker}.{field}")
        digest = row.get("per_ticker_canonical_dataset_chain_candidate_digest")
        _expect_digest(digest, f"{ticker}.candidate digest")
        _expect(digest, per_ticker_canonical_dataset_chain_candidate_digest_v1(row), f"{ticker}.candidate digest")


def validate_canonical_dataset_chain_candidate_v1(candidate: dict[str, Any]) -> dict[str, Any]:
    """Validate exact evidence, planning content, and closed authority gates."""
    if not isinstance(candidate, dict):
        raise CanonicalDatasetChainCandidateError("candidate must be an object")
    expected = {
        "artifact_kind": ARTIFACT_KIND_CANONICAL_DATASET_CHAIN_CANDIDATE,
        "schema_version": SCHEMA_VERSION_CANONICAL_DATASET_CHAIN_CANDIDATE_V1,
        "candidate_status": CANONICAL_DATASET_CHAIN_READY_FOR_OPERATOR_REVIEW,
        "acquisition_generation_freeze_digest": EXPECTED_ACQUISITION_GENERATION_FREEZE_DIGEST,
        "acquisition_generation_approval_digest": EXPECTED_ACQUISITION_GENERATION_APPROVAL_DIGEST,
        "acquisition_evidence_results_review_package_digest": EXPECTED_ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        "acquisition_provider_evidence_execution_digest": EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "acquisition_provider_evidence_request_approval_digest": EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST,
        "acquisition_generation_chain_candidate_review_package_digest": EXPECTED_ACQUISITION_GENERATION_CHAIN_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "corporate_action_authority_approval_digest": EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST,
        "combined_split_dividend_corporate_action_readiness_review_package_digest": EXPECTED_COMBINED_READINESS_REVIEW_PACKAGE_DIGEST,
        "split_event_authority_freeze_digest": EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST,
        "dividend_event_authority_freeze_digest": EXPECTED_DIVIDEND_EVENT_AUTHORITY_FREEZE_DIGEST,
        "identity_authority_freeze_digest": EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
        "ticker_universe_selection_approval_digest": EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST,
        "post_identity_freeze_registry_inventory_approval_digest": EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST,
        "source_acquisition_generation_freeze_blocker_count": 0,
        "target_universe": TARGET_UNIVERSE,
        "target_universe_count": 12,
        "canonical_dataset_chain_objective": CANONICAL_DATASET_CHAIN_OBJECTIVE,
        "canonical_dataset_chain_scope": CANONICAL_DATASET_CHAIN_SCOPE,
        "canonical_dataset_mode": CANONICAL_DATASET_MODE,
        "canonical_dataset_authority_status": CANONICAL_DATASET_AUTHORITY_STATUS,
        "canonical_dataset_planning_dimensions": CANONICAL_DATASET_PLANNING_DIMENSIONS,
        "canonical_dataset_source_profile": SOURCE_PROFILE,
        "future_canonical_dataset_chain": FUTURE_CANONICAL_DATASET_CHAIN,
        "future_gates": FUTURE_GATES,
        "risk_controls": RISK_CONTROLS,
        "planned_outputs": _planned_outputs(),
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": PROFITABILITY_NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "corporate_action_authority_scope": "CORPORATE_ACTION_AUTHORITY_ONLY",
        "split_event_authority_scope": "SPLIT_EVENT_AUTHORITY_ONLY",
        "dividend_event_authority_scope": "DIVIDEND_EVENT_AUTHORITY_ONLY",
    }
    for field, value in expected.items():
        _expect(candidate.get(field), value, field)
    for field in (
        "created_offline", "canonical_dataset_chain_candidate_created",
        "canonical_dataset_chain_ready_for_operator_review", "new_ticker_acquisition_authorized",
        "acquisition_generation_authorized", "acquisition_generation_approved", "acquisition_generation_frozen",
        "ready_for_canonical_dataset_chain_candidate", "corporate_action_authority_created",
        "corporate_action_authority_approved", "split_event_authority_created", "split_event_authority_frozen",
        "dividend_event_authority_created", "dividend_event_authority_frozen", "identity_authority_created",
        "identity_authority_frozen", "research_only", "operator_review_required", "meta_reduced_bar_count_preserved",
    ):
        _expect_true(candidate.get(field), field)
    for field in (
        "provider_requests_made", "live_provider_transport_enabled", "market_data_acquisition_performed",
        "dataset_generation_performed", "raw_provider_payloads_committed", "api_keys_stored_or_printed",
        "canonical_dataset_chain_approved", "dataset_generation_authorized", "canonical_dataset_authorized",
        "canonical_dataset_candidate_created", "canonical_dataset_generation_executed", "canonical_dataset_frozen",
        "registry_approval_created", "acquisition_generation_executed", "acquisition_generation_results_created",
        "additional_predictive_evidence_execution_authorized", "additional_predictive_evidence_executed",
        "predictive_experiment_rerun_authorized", "predictive_experiment_rerun_performed",
        "feature_matrix_regeneration_performed", "new_strategy_scoring_performed", "trade_recommendations_generated",
        "runtime_migration_approved", "runtime_migration_active", "automatic_stitching",
        "dataset_generation_artifact_created", "canonical_dataset_artifact_created",
        "registry_approval_artifact_created", "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_created", "runtime_migration_approval_created",
    ):
        _expect_false(candidate.get(field), field)
    _validate_per_ticker(candidate)
    checklist = candidate.get("candidate_checklist")
    if not isinstance(checklist, list):
        raise CanonicalDatasetChainCandidateError("candidate_checklist missing")
    _expect([row.get("check_id") for row in checklist], REQUIRED_CHECK_IDS, "candidate checklist ids")
    for row in checklist:
        _expect(row.get("status"), PASS, f"{row.get('check_id')}.status")
        _expect(row.get("severity"), BLOCKER, f"{row.get('check_id')}.severity")
    _expect(checklist, _checklist(candidate), "candidate checklist")
    _expect(candidate.get("candidate_summary"), _summary(checklist), "candidate summary")
    digest = candidate.get("canonical_dataset_chain_candidate_digest")
    _expect_digest(digest, "canonical_dataset_chain_candidate_digest")
    _expect(digest, canonical_dataset_chain_candidate_digest_v1(candidate), "canonical_dataset_chain_candidate_digest")
    return {
        "status": CANONICAL_DATASET_CHAIN_READY_FOR_OPERATOR_REVIEW,
        "canonical_dataset_chain_candidate_digest": digest,
        "total_checks": candidate["candidate_summary"]["total_checks"],
        "passed_checks": candidate["candidate_summary"]["passed_checks"],
        "failed_checks": candidate["candidate_summary"]["failed_checks"],
        "blocker_count": candidate["candidate_summary"]["blocker_count"],
    }


def build_canonical_dataset_chain_candidate_markdown_v1(candidate: dict[str, Any]) -> str:
    validation = validate_canonical_dataset_chain_candidate_v1(candidate)
    summary = candidate["candidate_summary"]
    lines = [
        "# MarketFlow Canonical Dataset Chain Candidate v1", "", "## Canonical Dataset Chain Candidate",
        f"- Artifact/status: `{candidate['artifact_kind']}` / `{candidate['candidate_status']}`.",
        f"- Candidate digest: `{validation['canonical_dataset_chain_candidate_digest']}`.", "",
        "## Source Acquisition Generation Freeze", f"- Freeze digest: `{candidate['acquisition_generation_freeze_digest']}`.", "",
        "## Target Universe", "- " + ", ".join(f"`{ticker}`" for ticker in candidate["target_universe"]) + ".", "",
        "## Per-Ticker Canonical Dataset Chain Candidate Entries",
    ]
    lines.extend(f"- `{row['ticker']}`: `{row['canonical_dataset_chain_status']}`, bars `{row['historical_bar_count']}`." for row in candidate["per_ticker_canonical_dataset_chain_candidates"])
    lines.extend([
        "", "## Canonical Dataset Planning Dimensions", *[f"- `{item}`" for item in candidate["canonical_dataset_planning_dimensions"]], "",
        "## Source Profile", *[f"- `{key}`: `{value}`." for key, value in candidate["canonical_dataset_source_profile"].items()], "",
        "## Future Canonical Dataset Chain", *[f"- {item}" for item in candidate["future_canonical_dataset_chain"]], "",
        "## Future Gates", *[f"- `{item}`" for item in candidate["future_gates"]], "",
        "## Risk Controls", *[f"- `{item}`" for item in candidate["risk_controls"]], "",
        "## Dataset Boundary", "- Dataset generation is neither authorized nor performed.", "",
        "## Canonical Dataset Boundary", "- No canonical dataset candidate, authorization, generation, or freeze was created.", "",
        "## Registry Boundary", "- No registry approval was created.", "",
        "## Predictive/Profitability Boundary", "- Predictive usefulness and profitability remain not accepted.", "",
        "## Runtime Boundary", "- Runtime, strategy, paper trading, and broker execution remain `NOT_AUTHORIZED`.", "",
        "## Checklist Summary", f"- Total/passed/failed/blockers: `{summary['total_checks']} / {summary['passed_checks']} / {summary['failed_checks']} / {summary['blocker_count']}`.", "",
        "## Guardrails", "- This is an offline, research-only planning candidate requiring separate operator review.",
        "- No provider request, market-data acquisition, dataset generation, canonical dataset, registry approval, predictive acceptance, or runtime activation occurred.",
    ])
    return "\n".join(lines) + "\n"


def write_canonical_dataset_chain_candidate_v1(output_dir: str | Path) -> dict[str, Any]:
    """Write canonical candidate JSON without overwriting an existing artifact."""
    candidate = build_canonical_dataset_chain_candidate_v1()
    validation = validate_canonical_dataset_chain_candidate_v1(candidate)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "canonical_dataset_chain_candidate_v1.json"
    if path.exists():
        raise CanonicalDatasetChainCandidateError("canonical dataset chain candidate output already exists")
    payload = canonical_json_bytes(candidate)
    path.write_bytes(payload)
    return {
        "path": str(path),
        "artifact_kind": candidate["artifact_kind"],
        "candidate_status": candidate["candidate_status"],
        "canonical_dataset_chain_candidate_digest": validation["canonical_dataset_chain_candidate_digest"],
        "payload_sha256": sha256_bytes(payload),
    }
