"""Offline operator-attested approval of the frozen dataset for research registry use."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import research_registry_candidate_operator_review_service as review_service


ARTIFACT_KIND_RESEARCH_REGISTRY_APPROVED = "RESEARCH_REGISTRY_APPROVED"
SCHEMA_VERSION_RESEARCH_REGISTRY_APPROVAL_V1 = "research_registry_approval_v1"
RESEARCH_REGISTRY_APPROVED = "RESEARCH_REGISTRY_APPROVED"
RESEARCH_REGISTRY_APPROVAL_ONLY = "RESEARCH_REGISTRY_APPROVAL_ONLY"
APPROVED_FOR_RESEARCH_REGISTRY_ONLY = "APPROVED_FOR_RESEARCH_REGISTRY_ONLY"
OPERATOR_DECISION_APPROVE_RESEARCH_REGISTRY = "APPROVE_RESEARCH_REGISTRY"
OPERATOR_ATTESTATION_VERSION_RESEARCH_REGISTRY_APPROVAL_V1 = (
    "research_registry_approval_operator_attestation_v1"
)
REQUIRED_RESEARCH_REGISTRY_APPROVAL_ATTESTATION_PHRASE = (
    "APPROVE RESEARCH REGISTRY MSFT NVDA AMZN GOOGL META TSLA JPM XOM JNJ WMT "
    "CAT LMT RESEARCH_REGISTRY_APPROVAL_ONLY"
)

EXPECTED_RESEARCH_REGISTRY_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    "5ec5c7a36787963e14e23494cee7fad54a4d072d613b06dccc1e43792d94b267"
)
EXPECTED_RESEARCH_REGISTRY_CANDIDATE_DIGEST = (
    review_service.EXPECTED_REVIEWED_RESEARCH_REGISTRY_CANDIDATE_DIGEST
)
EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST = (
    review_service.candidate_service.EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST
)
EXPECTED_CANONICAL_DATASET_RESULTS_REVIEW_PACKAGE_DIGEST = (
    review_service.candidate_service.EXPECTED_CANONICAL_DATASET_RESULTS_REVIEW_PACKAGE_DIGEST
)
EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST = (
    review_service.candidate_service.EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST
)
EXPECTED_CANONICAL_DATASET_GENERATION_APPROVAL_DIGEST = (
    review_service.candidate_service.EXPECTED_CANONICAL_DATASET_GENERATION_APPROVAL_DIGEST
)
EXPECTED_ACQUISITION_GENERATION_FREEZE_DIGEST = (
    review_service.candidate_service.EXPECTED_ACQUISITION_GENERATION_FREEZE_DIGEST
)
EXPECTED_ACQUISITION_GENERATION_APPROVAL_DIGEST = (
    review_service.candidate_service.EXPECTED_ACQUISITION_GENERATION_APPROVAL_DIGEST
)
EXPECTED_ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST = (
    review_service.candidate_service.EXPECTED_ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST
)
EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST = (
    review_service.candidate_service.EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST
)
EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST = (
    review_service.candidate_service.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST
)
EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST = (
    review_service.candidate_service.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST
)
EXPECTED_RECORDS_DIGEST = review_service.candidate_service.EXPECTED_RECORDS_DIGEST

TARGET_UNIVERSE = list(review_service.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(review_service.EXPECTED_RECORD_COUNTS)
NOT_ACCEPTED = review_service.NOT_ACCEPTED
NOT_AUTHORIZED = review_service.NOT_AUTHORIZED
PASS = review_service.PASS
FAIL = review_service.FAIL
BLOCKER = review_service.BLOCKER

APPROVED_REGISTRY_METADATA = deepcopy(review_service.REGISTRY_CANDIDATE_METADATA)
APPROVED_REGISTRY_METADATA.pop("registry_candidate_label")
APPROVED_REGISTRY_METADATA.update(
    {
        "registry_label": review_service.candidate_service.RESEARCH_ONLY_NON_ACTIONABLE,
        "registry_entry_status": APPROVED_FOR_RESEARCH_REGISTRY_ONLY,
    }
)

LIMITATIONS = [
    "registry_approval_is_not_predictive_usefulness_acceptance",
    "registry_approval_is_not_profitability_acceptance",
    "registry_approval_is_not_runtime_authorization",
    "registry_approval_is_not_strategy_authorization",
    "registry_approval_is_not_paper_trading_authorization",
    "registry_approval_is_not_broker_execution_authorization",
    "frozen_canonical_dataset_must_not_be_mutated",
    "meta_reduced_record_count_preserved",
    "no_missing_bar_fabrication",
    "operator_approval_required_before_additional_predictive_evidence_execution",
    "operator_approval_required_before_runtime_migration_if_ever_authorized",
]
NEXT_GATES = [
    "additional_predictive_evidence_chain_candidate",
    "additional_predictive_evidence_chain_candidate_operator_review",
    "additional_predictive_evidence_execution_approval_if_required",
    "predictive_usefulness_reassessment_if_required",
    "profitability_review_chain_if_required",
    "runtime_migration_chain_if_ever_authorized",
]

REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS = [
    "operator_confirms_dataset_scope_research_only",
    "operator_confirms_meta_reduced_record_count_preserved",
    "operator_confirms_approval_scope_research_registry_only",
    "operator_confirms_research_registry_approved",
    "operator_confirms_registry_approval_created",
    "operator_confirms_ready_for_additional_predictive_evidence_chain_candidate",
    "operator_confirms_no_predictive_usefulness_acceptance",
    "operator_confirms_no_profitability_acceptance",
    "operator_confirms_no_runtime_migration_approval",
    "operator_confirms_no_runtime_activation",
    "operator_confirms_no_strategy_authorization",
    "operator_confirms_no_paper_trading",
    "operator_confirms_no_broker_execution",
    "operator_confirms_no_trade_recommendations",
    "operator_confirms_no_api_key_storage_or_printing",
    "operator_confirms_no_raw_payload_commit",
]

REQUIRED_CHECK_IDS = [
    "research_registry_candidate_review_digest_matches_expected",
    "research_registry_candidate_review_has_zero_blockers",
    "research_registry_candidate_digest_bound",
    "canonical_dataset_freeze_digest_bound",
    "canonical_dataset_results_review_digest_bound",
    "canonical_dataset_generation_digest_bound",
    "records_digest_bound",
    "identity_freeze_digest_bound",
    "target_universe_count_12",
    "target_universe_matches_registry_candidate_universe",
    "operator_decision_approved",
    "operator_attestation_phrase_matches",
    "operator_confirms_all_source_digests",
    "operator_confirms_dataset_name",
    "operator_confirms_dataset_scope_research_only",
    "operator_confirms_total_canonical_record_count_11946",
    "operator_confirms_records_digest",
    "operator_confirms_meta_reduced_record_count_preserved",
    "approval_scope_research_registry_only",
    "research_registry_approved_true",
    "registry_approval_created_true",
    "ready_for_additional_predictive_evidence_chain_candidate_true",
    "per_ticker_research_registry_approval_entries_12",
    "per_ticker_research_registry_approval_digests_present",
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
    "market_data_acquisition_performed_in_approval_false",
    "dataset_generation_performed_in_approval_false",
    "canonical_dataset_regenerated_in_approval_false",
    "raw_provider_payloads_not_committed",
    "api_keys_not_stored_or_printed",
    "approval_creates_predictive_usefulness_acceptance_false",
    "approval_creates_profitability_acceptance_false",
    "approval_creates_runtime_authority_false",
    "limitations_recorded",
    "next_gates_defined",
    "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created",
    "no_runtime_migration_approval_created",
]


class ResearchRegistryApprovalError(ValueError):
    """Raised when registry approval evidence or attestation is invalid."""


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise ResearchRegistryApprovalError(f"{field} mismatch")


def _expect_true(actual: Any, field: str) -> None:
    if actual is not True:
        raise ResearchRegistryApprovalError(f"{field} must be true")


def _expect_false(actual: Any, field: str) -> None:
    if actual is not False:
        raise ResearchRegistryApprovalError(f"{field} must be false")


def _expect_digest(actual: Any, field: str) -> None:
    if not isinstance(actual, str) or len(actual) != 64:
        raise ResearchRegistryApprovalError(f"{field} missing")


def build_research_registry_approval_attestation_v1(
    *,
    operator_reference: str,
    operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str,
    operator_confirms_research_registry_candidate_review_digest: str,
    operator_confirms_research_registry_candidate_digest: str,
    operator_confirms_canonical_dataset_freeze_digest: str,
    operator_confirms_canonical_dataset_results_review_digest: str,
    operator_confirms_canonical_dataset_generation_digest: str,
    operator_confirms_identity_freeze_digest: str,
    operator_confirms_target_universe: list[str],
    operator_confirms_target_count: int,
    operator_confirms_dataset_name: str,
    operator_confirms_dataset_scope_research_only: bool,
    operator_confirms_total_canonical_record_count: int,
    operator_confirms_records_digest: str,
    operator_confirms_meta_reduced_record_count_preserved: bool,
    operator_confirms_approval_scope_research_registry_only: bool,
    operator_confirms_research_registry_approved: bool,
    operator_confirms_registry_approval_created: bool,
    operator_confirms_ready_for_additional_predictive_evidence_chain_candidate: bool,
    operator_confirms_no_predictive_usefulness_acceptance: bool,
    operator_confirms_no_profitability_acceptance: bool,
    operator_confirms_no_runtime_migration_approval: bool,
    operator_confirms_no_runtime_activation: bool,
    operator_confirms_no_strategy_authorization: bool,
    operator_confirms_no_paper_trading: bool,
    operator_confirms_no_broker_execution: bool,
    operator_confirms_no_trade_recommendations: bool,
    operator_confirms_no_api_key_storage_or_printing: bool,
    operator_confirms_no_raw_payload_commit: bool,
    operator_decision: str = OPERATOR_DECISION_APPROVE_RESEARCH_REGISTRY,
) -> dict[str, Any]:
    """Build a non-secret attestation; exact validation occurs at approval."""
    return {name: deepcopy(value) for name, value in locals().items()} | {
        "operator_attestation_version": (
            OPERATOR_ATTESTATION_VERSION_RESEARCH_REGISTRY_APPROVAL_V1
        )
    }


def _expected_digest_confirmations() -> dict[str, str]:
    return {
        "operator_confirms_research_registry_candidate_review_digest": EXPECTED_RESEARCH_REGISTRY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "operator_confirms_research_registry_candidate_digest": EXPECTED_RESEARCH_REGISTRY_CANDIDATE_DIGEST,
        "operator_confirms_canonical_dataset_freeze_digest": EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST,
        "operator_confirms_canonical_dataset_results_review_digest": EXPECTED_CANONICAL_DATASET_RESULTS_REVIEW_PACKAGE_DIGEST,
        "operator_confirms_canonical_dataset_generation_digest": EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST,
        "operator_confirms_identity_freeze_digest": EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
    }


def _validate_attestation(attestation: Mapping[str, Any]) -> None:
    if not isinstance(attestation, Mapping):
        raise ResearchRegistryApprovalError("operator_attestation missing")
    expected = {
        "operator_decision": OPERATOR_DECISION_APPROVE_RESEARCH_REGISTRY,
        "operator_attestation_phrase": REQUIRED_RESEARCH_REGISTRY_APPROVAL_ATTESTATION_PHRASE,
        "operator_attestation_version": OPERATOR_ATTESTATION_VERSION_RESEARCH_REGISTRY_APPROVAL_V1,
        "operator_confirms_target_universe": TARGET_UNIVERSE,
        "operator_confirms_target_count": 12,
        "operator_confirms_dataset_name": "expanded_universe_canonical_dataset_v1",
        "operator_confirms_total_canonical_record_count": 11946,
        "operator_confirms_records_digest": EXPECTED_RECORDS_DIGEST,
        **_expected_digest_confirmations(),
    }
    for field, value in expected.items():
        _expect(attestation.get(field), value, field)
    for field in REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS:
        _expect_true(attestation.get(field), field)
    for field in ("operator_reference", "operator_attestation_timestamp_utc"):
        value = attestation.get(field)
        if not isinstance(value, str) or not value.strip():
            raise ResearchRegistryApprovalError(f"{field} missing")


def _source_review(package: dict[str, Any] | None) -> dict[str, Any]:
    source = (
        review_service.build_research_registry_candidate_review_package_v1()
        if package is None
        else deepcopy(package)
    )
    try:
        validation = review_service.validate_research_registry_candidate_review_package_v1(
            source
        )
    except review_service.ResearchRegistryCandidateReviewPackageError as exc:
        raise ResearchRegistryApprovalError("candidate review package invalid") from exc
    _expect(
        validation["research_registry_candidate_review_package_digest"],
        EXPECTED_RESEARCH_REGISTRY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "research registry candidate review digest",
    )
    _expect(validation["blocker_count"], 0, "research registry candidate review blockers")
    return source


def per_ticker_research_registry_approval_digest_v1(entry: dict[str, Any]) -> str:
    payload = deepcopy(entry)
    payload.pop("per_ticker_research_registry_approval_digest", None)
    return semantic_digest(payload)


def _per_ticker_approval_entries(source: dict[str, Any]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for reviewed in source["per_ticker_research_registry_review_entries"]:
        entry = {
            "ticker": reviewed["ticker"],
            "identity_authority_status": reviewed["identity_authority_status"],
            "corporate_action_authority_status": reviewed[
                "corporate_action_authority_status"
            ],
            "acquisition_generation_status": reviewed["acquisition_generation_status"],
            "canonical_dataset_status": reviewed["canonical_dataset_status"],
            "research_registry_candidate_status": reviewed[
                "research_registry_candidate_status"
            ],
            "research_registry_candidate_review_status": reviewed[
                "research_registry_candidate_review_status"
            ],
            "research_registry_approval_status": APPROVED_FOR_RESEARCH_REGISTRY_ONLY,
            "historical_record_count": reviewed["historical_record_count"],
            "meta_reduced_record_count_flag": reviewed[
                "meta_reduced_record_count_flag"
            ],
            "predictive_usefulness": NOT_ACCEPTED,
            "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "source_research_registry_candidate_review_digest": (
                EXPECTED_RESEARCH_REGISTRY_CANDIDATE_REVIEW_PACKAGE_DIGEST
            ),
            "source_research_registry_candidate_digest": (
                EXPECTED_RESEARCH_REGISTRY_CANDIDATE_DIGEST
            ),
        }
        entry["per_ticker_research_registry_approval_digest"] = (
            per_ticker_research_registry_approval_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _base_artifact(source: dict[str, Any], attestation: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_RESEARCH_REGISTRY_APPROVED,
        "schema_version": SCHEMA_VERSION_RESEARCH_REGISTRY_APPROVAL_V1,
        "approval_status": RESEARCH_REGISTRY_APPROVED,
        "approval_scope": RESEARCH_REGISTRY_APPROVAL_ONLY,
        "created_offline": True,
        "provider_requests_made_in_approval": False,
        "live_provider_transport_enabled_in_approval": False,
        "market_data_acquisition_performed_in_approval": False,
        "dataset_generation_performed_in_approval": False,
        "canonical_dataset_regenerated_in_approval": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "research_registry_candidate_created": True,
        "research_registry_candidate_review_created": True,
        "research_registry_candidate_ready_for_operator_review": True,
        "research_registry_approved": True,
        "registry_approval_created": True,
        "ready_for_additional_predictive_evidence_chain_candidate": True,
        "canonical_dataset_generated": True,
        "canonical_dataset_frozen": True,
        "canonical_dataset_freeze_scope": source["canonical_dataset_freeze_scope"],
        "ready_for_research_registry_candidate": True,
        "dataset_generation_authorized": True,
        "canonical_dataset_authorized": True,
        "canonical_dataset_generation_approved": True,
        "new_ticker_acquisition_authorized": True,
        "acquisition_generation_authorized": True,
        "acquisition_generation_approved": True,
        "acquisition_generation_frozen": True,
        "corporate_action_authority_created": True,
        "corporate_action_authority_approved": True,
        "corporate_action_authority_scope": source["corporate_action_authority_scope"],
        "split_event_authority_created": True,
        "split_event_authority_frozen": True,
        "split_event_authority_scope": source["split_event_authority_scope"],
        "dividend_event_authority_created": True,
        "dividend_event_authority_frozen": True,
        "dividend_event_authority_scope": source["dividend_event_authority_scope"],
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
        "profitability": NOT_ACCEPTED,
        "runtime_migration_approved": False,
        "runtime_migration_active": False,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "automatic_stitching": False,
        "research_registry_candidate_review_package_digest": source[
            "research_registry_candidate_review_package_digest"
        ],
        "research_registry_candidate_digest": source[
            "reviewed_research_registry_candidate_digest"
        ],
        "source_research_registry_candidate_review_blocker_count": source[
            "review_summary"
        ]["blocker_count"],
        "canonical_dataset_freeze_digest": source["canonical_dataset_freeze_digest"],
        "canonical_dataset_results_review_package_digest": source[
            "canonical_dataset_results_review_package_digest"
        ],
        "canonical_dataset_generation_digest": source[
            "canonical_dataset_generation_digest"
        ],
        "canonical_dataset_generation_approval_digest": source[
            "canonical_dataset_generation_approval_digest"
        ],
        "acquisition_generation_freeze_digest": source[
            "acquisition_generation_freeze_digest"
        ],
        "acquisition_generation_approval_digest": source[
            "acquisition_generation_approval_digest"
        ],
        "acquisition_evidence_results_review_package_digest": source[
            "acquisition_evidence_results_review_package_digest"
        ],
        "corporate_action_authority_approval_digest": source[
            "corporate_action_authority_approval_digest"
        ],
        "identity_authority_freeze_digest": source["identity_authority_freeze_digest"],
        "ticker_universe_selection_approval_digest": source[
            "ticker_universe_selection_approval_digest"
        ],
        "target_universe": list(source["target_universe"]),
        "target_universe_count": source["target_universe_count"],
        "source_profile": deepcopy(source["source_profile"]),
        "total_canonical_record_count": source["total_canonical_record_count"],
        "records_digest": source["records_digest"],
        "per_ticker_record_counts": deepcopy(source["per_ticker_record_counts"]),
        "data_quality_status": source["data_quality_status"],
        "approved_registry_metadata": deepcopy(APPROVED_REGISTRY_METADATA),
        "per_ticker_research_registry_approvals": _per_ticker_approval_entries(source),
        "research_registry_approved_by_operator": True,
        "registry_approval_scope": RESEARCH_REGISTRY_APPROVAL_ONLY,
        "registry_approval_creates_predictive_usefulness_acceptance": False,
        "registry_approval_creates_profitability_acceptance": False,
        "registry_approval_creates_runtime_authority": False,
        "registry_approval_creates_strategy_authority": False,
        "registry_approval_creates_paper_trading_authority": False,
        "registry_approval_creates_broker_execution_authority": False,
        "limitations": list(LIMITATIONS),
        "next_gates": list(NEXT_GATES),
        "operator_attestation": deepcopy(dict(attestation)),
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
    }


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


def _checklist(artifact: dict[str, Any]) -> list[dict[str, Any]]:
    operator = artifact.get("operator_attestation", {})
    entries = artifact.get("per_ticker_research_registry_approvals", [])
    values: dict[str, tuple[Any, Any]] = {
        "research_registry_candidate_review_digest_matches_expected": (EXPECTED_RESEARCH_REGISTRY_CANDIDATE_REVIEW_PACKAGE_DIGEST, artifact.get("research_registry_candidate_review_package_digest")),
        "research_registry_candidate_review_has_zero_blockers": (0, artifact.get("source_research_registry_candidate_review_blocker_count")),
        "research_registry_candidate_digest_bound": (EXPECTED_RESEARCH_REGISTRY_CANDIDATE_DIGEST, artifact.get("research_registry_candidate_digest")),
        "canonical_dataset_freeze_digest_bound": (EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST, artifact.get("canonical_dataset_freeze_digest")),
        "canonical_dataset_results_review_digest_bound": (EXPECTED_CANONICAL_DATASET_RESULTS_REVIEW_PACKAGE_DIGEST, artifact.get("canonical_dataset_results_review_package_digest")),
        "canonical_dataset_generation_digest_bound": (EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST, artifact.get("canonical_dataset_generation_digest")),
        "records_digest_bound": (EXPECTED_RECORDS_DIGEST, artifact.get("records_digest")),
        "identity_freeze_digest_bound": (EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST, artifact.get("identity_authority_freeze_digest")),
        "target_universe_count_12": (12, artifact.get("target_universe_count")),
        "target_universe_matches_registry_candidate_universe": (TARGET_UNIVERSE, artifact.get("target_universe")),
        "operator_decision_approved": (OPERATOR_DECISION_APPROVE_RESEARCH_REGISTRY, operator.get("operator_decision")),
        "operator_attestation_phrase_matches": (REQUIRED_RESEARCH_REGISTRY_APPROVAL_ATTESTATION_PHRASE, operator.get("operator_attestation_phrase")),
        "operator_confirms_all_source_digests": (True, all(operator.get(field) == value for field, value in _expected_digest_confirmations().items())),
        "operator_confirms_dataset_name": ("expanded_universe_canonical_dataset_v1", operator.get("operator_confirms_dataset_name")),
        "operator_confirms_dataset_scope_research_only": (True, operator.get("operator_confirms_dataset_scope_research_only")),
        "operator_confirms_total_canonical_record_count_11946": (11946, operator.get("operator_confirms_total_canonical_record_count")),
        "operator_confirms_records_digest": (EXPECTED_RECORDS_DIGEST, operator.get("operator_confirms_records_digest")),
        "operator_confirms_meta_reduced_record_count_preserved": (True, operator.get("operator_confirms_meta_reduced_record_count_preserved")),
        "approval_scope_research_registry_only": (RESEARCH_REGISTRY_APPROVAL_ONLY, artifact.get("approval_scope")),
        "research_registry_approved_true": (True, artifact.get("research_registry_approved")),
        "registry_approval_created_true": (True, artifact.get("registry_approval_created")),
        "ready_for_additional_predictive_evidence_chain_candidate_true": (True, artifact.get("ready_for_additional_predictive_evidence_chain_candidate")),
        "per_ticker_research_registry_approval_entries_12": (12, len(entries)),
        "per_ticker_research_registry_approval_digests_present": (True, len(entries) == 12 and all(isinstance(row.get("per_ticker_research_registry_approval_digest"), str) and len(row["per_ticker_research_registry_approval_digest"]) == 64 for row in entries)),
        "predictive_usefulness_not_accepted": (NOT_ACCEPTED, artifact.get("predictive_usefulness")),
        "profitability_not_accepted": (NOT_ACCEPTED, artifact.get("profitability")),
        "runtime_use_not_authorized": (NOT_AUTHORIZED, artifact.get("runtime_use")),
        "strategy_use_not_authorized": (NOT_AUTHORIZED, artifact.get("strategy_use")),
        "paper_trading_not_authorized": (NOT_AUTHORIZED, artifact.get("paper_trading")),
        "broker_execution_not_authorized": (NOT_AUTHORIZED, artifact.get("broker_execution")),
        "limitations_recorded": (LIMITATIONS, artifact.get("limitations")),
        "next_gates_defined": (NEXT_GATES, artifact.get("next_gates")),
    }
    false_checks = {
        "additional_predictive_evidence_execution_authorized_false": "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed_false": "additional_predictive_evidence_executed",
        "predictive_experiment_rerun_authorized_false": "predictive_experiment_rerun_authorized",
        "new_strategy_scoring_performed_false": "new_strategy_scoring_performed",
        "trade_recommendations_generated_false": "trade_recommendations_generated",
        "runtime_migration_approved_false": "runtime_migration_approved",
        "automatic_stitching_false": "automatic_stitching",
        "provider_requests_made_in_approval_false": "provider_requests_made_in_approval",
        "live_provider_transport_enabled_in_approval_false": "live_provider_transport_enabled_in_approval",
        "market_data_acquisition_performed_in_approval_false": "market_data_acquisition_performed_in_approval",
        "dataset_generation_performed_in_approval_false": "dataset_generation_performed_in_approval",
        "canonical_dataset_regenerated_in_approval_false": "canonical_dataset_regenerated_in_approval",
        "raw_provider_payloads_not_committed": "raw_provider_payloads_committed",
        "api_keys_not_stored_or_printed": "api_keys_stored_or_printed",
        "approval_creates_predictive_usefulness_acceptance_false": "registry_approval_creates_predictive_usefulness_acceptance",
        "approval_creates_profitability_acceptance_false": "registry_approval_creates_profitability_acceptance",
        "approval_creates_runtime_authority_false": "registry_approval_creates_runtime_authority",
        "no_predictive_usefulness_acceptance_artifact_created": "predictive_usefulness_acceptance_artifact_created",
        "no_profitability_acceptance_created": "profitability_acceptance_created",
        "no_runtime_migration_approval_created": "runtime_migration_approval_created",
    }
    values.update({check_id: (False, artifact.get(field)) for check_id, field in false_checks.items()})
    return [_check(check_id, *values[check_id]) for check_id in REQUIRED_CHECK_IDS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [row for row in checklist if row.get("status") != PASS]
    approved = not failed
    return {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row.get("severity") == BLOCKER for row in failed),
        "research_registry_approved_by_operator": approved,
        "approval_scope": RESEARCH_REGISTRY_APPROVAL_ONLY,
        "research_registry_approved": approved,
        "registry_approval_created": approved,
        "ready_for_additional_predictive_evidence_chain_candidate": approved,
        "additional_predictive_evidence_execution_authorized": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def research_registry_approval_digest_v1(approved_artifact: dict[str, Any]) -> str:
    payload = deepcopy(approved_artifact)
    payload.pop("research_registry_approval_digest", None)
    return semantic_digest(payload)


def build_research_registry_approved_v1(
    *,
    research_registry_candidate_review_package: dict[str, Any] | None = None,
    operator_attestation: dict[str, Any],
) -> dict[str, Any]:
    """Build registry approval only after validating every explicit confirmation."""
    source = _source_review(research_registry_candidate_review_package)
    _validate_attestation(operator_attestation)
    artifact = _base_artifact(source, operator_attestation)
    artifact["approval_checklist"] = _checklist(artifact)
    artifact["approval_summary"] = _summary(artifact["approval_checklist"])
    artifact["research_registry_approval_digest"] = research_registry_approval_digest_v1(
        artifact
    )
    validate_research_registry_approved_v1(artifact)
    return artifact


def _validate_per_ticker(artifact: dict[str, Any]) -> None:
    entries = artifact.get("per_ticker_research_registry_approvals")
    if not isinstance(entries, list) or len(entries) != 12:
        raise ResearchRegistryApprovalError("per-ticker registry approvals mismatch")
    _expect([row.get("ticker") for row in entries], TARGET_UNIVERSE, "per-ticker order")
    for row in entries:
        ticker = row["ticker"]
        expected = {
            "identity_authority_status": "FROZEN",
            "corporate_action_authority_status": "APPROVED",
            "acquisition_generation_status": "FROZEN",
            "canonical_dataset_status": "FROZEN",
            "research_registry_candidate_status": review_service.candidate_service.PLANNED_READY_FOR_OPERATOR_REVIEW,
            "research_registry_candidate_review_status": review_service.READY_FOR_OPERATOR_ASSESSMENT,
            "research_registry_approval_status": APPROVED_FOR_RESEARCH_REGISTRY_ONLY,
            "historical_record_count": EXPECTED_RECORD_COUNTS[ticker],
            "meta_reduced_record_count_flag": ticker == "META",
            "predictive_usefulness": NOT_ACCEPTED,
            "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "source_research_registry_candidate_review_digest": EXPECTED_RESEARCH_REGISTRY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
            "source_research_registry_candidate_digest": EXPECTED_RESEARCH_REGISTRY_CANDIDATE_DIGEST,
        }
        for field, value in expected.items():
            _expect(row.get(field), value, f"{ticker}.{field}")
        digest = row.get("per_ticker_research_registry_approval_digest")
        _expect_digest(digest, f"{ticker}.per_ticker_research_registry_approval_digest")
        _expect(
            digest,
            per_ticker_research_registry_approval_digest_v1(row),
            f"{ticker}.approval digest",
        )


def validate_research_registry_approved_v1(
    approved_artifact: dict[str, Any],
) -> dict[str, Any]:
    """Validate approval, attestation, exact evidence bindings, and closed gates."""
    if not isinstance(approved_artifact, dict):
        raise ResearchRegistryApprovalError("approved_artifact must be an object")
    expected = {
        "artifact_kind": ARTIFACT_KIND_RESEARCH_REGISTRY_APPROVED,
        "schema_version": SCHEMA_VERSION_RESEARCH_REGISTRY_APPROVAL_V1,
        "approval_status": RESEARCH_REGISTRY_APPROVED,
        "approval_scope": RESEARCH_REGISTRY_APPROVAL_ONLY,
        "registry_approval_scope": RESEARCH_REGISTRY_APPROVAL_ONLY,
        "research_registry_candidate_review_package_digest": EXPECTED_RESEARCH_REGISTRY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "research_registry_candidate_digest": EXPECTED_RESEARCH_REGISTRY_CANDIDATE_DIGEST,
        "source_research_registry_candidate_review_blocker_count": 0,
        "canonical_dataset_freeze_digest": EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST,
        "canonical_dataset_results_review_package_digest": EXPECTED_CANONICAL_DATASET_RESULTS_REVIEW_PACKAGE_DIGEST,
        "canonical_dataset_generation_digest": EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST,
        "canonical_dataset_generation_approval_digest": EXPECTED_CANONICAL_DATASET_GENERATION_APPROVAL_DIGEST,
        "acquisition_generation_freeze_digest": EXPECTED_ACQUISITION_GENERATION_FREEZE_DIGEST,
        "acquisition_generation_approval_digest": EXPECTED_ACQUISITION_GENERATION_APPROVAL_DIGEST,
        "acquisition_evidence_results_review_package_digest": EXPECTED_ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        "corporate_action_authority_approval_digest": EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST,
        "identity_authority_freeze_digest": EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
        "ticker_universe_selection_approval_digest": EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST,
        "canonical_dataset_freeze_scope": review_service.candidate_service.freeze.CANONICAL_DATASET_FREEZE_ONLY,
        "target_universe": TARGET_UNIVERSE,
        "target_universe_count": 12,
        "source_profile": review_service.candidate_service.SOURCE_PROFILE,
        "total_canonical_record_count": 11946,
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "per_ticker_record_counts": EXPECTED_RECORD_COUNTS,
        "data_quality_status": "PASS_WITH_PRESERVED_SOURCE_LIMITATION",
        "approved_registry_metadata": APPROVED_REGISTRY_METADATA,
        "corporate_action_authority_scope": "CORPORATE_ACTION_AUTHORITY_ONLY",
        "split_event_authority_scope": "SPLIT_EVENT_AUTHORITY_ONLY",
        "dividend_event_authority_scope": "DIVIDEND_EVENT_AUTHORITY_ONLY",
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "limitations": LIMITATIONS,
        "next_gates": NEXT_GATES,
    }
    for field, value in expected.items():
        _expect(approved_artifact.get(field), value, field)
    for field in (
        "created_offline",
        "research_registry_candidate_created",
        "research_registry_candidate_review_created",
        "research_registry_candidate_ready_for_operator_review",
        "research_registry_approved",
        "registry_approval_created",
        "ready_for_additional_predictive_evidence_chain_candidate",
        "canonical_dataset_generated",
        "canonical_dataset_frozen",
        "ready_for_research_registry_candidate",
        "dataset_generation_authorized",
        "canonical_dataset_authorized",
        "canonical_dataset_generation_approved",
        "new_ticker_acquisition_authorized",
        "acquisition_generation_authorized",
        "acquisition_generation_approved",
        "acquisition_generation_frozen",
        "corporate_action_authority_created",
        "corporate_action_authority_approved",
        "split_event_authority_created",
        "split_event_authority_frozen",
        "dividend_event_authority_created",
        "dividend_event_authority_frozen",
        "identity_authority_created",
        "identity_authority_frozen",
        "research_only",
        "research_registry_approved_by_operator",
    ):
        _expect_true(approved_artifact.get(field), field)
    for field in (
        "provider_requests_made_in_approval",
        "live_provider_transport_enabled_in_approval",
        "market_data_acquisition_performed_in_approval",
        "dataset_generation_performed_in_approval",
        "canonical_dataset_regenerated_in_approval",
        "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
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
        "registry_approval_creates_predictive_usefulness_acceptance",
        "registry_approval_creates_profitability_acceptance",
        "registry_approval_creates_runtime_authority",
        "registry_approval_creates_strategy_authority",
        "registry_approval_creates_paper_trading_authority",
        "registry_approval_creates_broker_execution_authority",
        "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_created",
        "runtime_migration_approval_created",
    ):
        _expect_false(approved_artifact.get(field), field)
    _validate_attestation(approved_artifact.get("operator_attestation", {}))
    _validate_per_ticker(approved_artifact)
    checklist = approved_artifact.get("approval_checklist")
    if not isinstance(checklist, list):
        raise ResearchRegistryApprovalError("approval_checklist missing")
    _expect([row.get("check_id") for row in checklist], REQUIRED_CHECK_IDS, "approval checklist ids")
    _expect(checklist, _checklist(approved_artifact), "approval checklist")
    if any(row.get("status") != PASS or row.get("severity") != BLOCKER for row in checklist):
        raise ResearchRegistryApprovalError("approval checklist must pass")
    _expect(approved_artifact.get("approval_summary"), _summary(checklist), "approval_summary")
    digest = approved_artifact.get("research_registry_approval_digest")
    _expect_digest(digest, "research_registry_approval_digest")
    _expect(digest, research_registry_approval_digest_v1(approved_artifact), "research_registry_approval_digest")
    summary = approved_artifact["approval_summary"]
    return {
        "status": RESEARCH_REGISTRY_APPROVED,
        "research_registry_approval_digest": digest,
        "total_checks": summary["total_checks"],
        "passed_checks": summary["passed_checks"],
        "failed_checks": summary["failed_checks"],
        "blocker_count": summary["blocker_count"],
        "research_registry_approved": True,
        "registry_approval_created": True,
        "ready_for_additional_predictive_evidence_chain_candidate": True,
    }


def build_research_registry_approved_markdown_v1(
    approved_artifact: dict[str, Any],
) -> str:
    """Render sanitized registry approval evidence and remaining boundaries."""
    validation = validate_research_registry_approved_v1(approved_artifact)
    operator = approved_artifact["operator_attestation"]
    sections = [
        ("Approved Research Registry Entry", [f"Artifact/status/scope: `{approved_artifact['artifact_kind']}` / `{validation['status']}` / `{approved_artifact['approval_scope']}`.", f"Approval digest: `{validation['research_registry_approval_digest']}`."]),
        ("Operator Attestation", [f"Reference/version/timestamp: `{operator['operator_reference']}` / `{operator['operator_attestation_version']}` / `{operator['operator_attestation_timestamp_utc']}`.", "The required non-secret attestation phrase and confirmations were validated exactly."]),
        ("Source Research Registry Candidate Review", [f"Review/candidate digests: `{approved_artifact['research_registry_candidate_review_package_digest']}` / `{approved_artifact['research_registry_candidate_digest']}`."]),
        ("Source Frozen Canonical Dataset", [f"Freeze/review/generation digests: `{approved_artifact['canonical_dataset_freeze_digest']}` / `{approved_artifact['canonical_dataset_results_review_package_digest']}` / `{approved_artifact['canonical_dataset_generation_digest']}`."]),
        ("Target Universe", [", ".join(f"`{ticker}`" for ticker in approved_artifact["target_universe"]) + "."]),
        ("Approved Registry Metadata", [f"`{key}`: `{value}`." for key, value in approved_artifact["approved_registry_metadata"].items()]),
        ("Per-Ticker Registry Approval Entries", [f"`{row['ticker']}`: `{row['research_registry_approval_status']}`, `{row['historical_record_count']}` records." for row in approved_artifact["per_ticker_research_registry_approvals"]]),
        ("Records Digest", [f"`{approved_artifact['records_digest']}`."]),
        ("META Reduced Record Count Preservation", ["META remains exactly `913` records; every other ticker remains exactly `1003`."]),
        ("Approval Scope", ["Approval is limited to research-registry admission and readiness for a future additional-evidence chain candidate."]),
        ("Predictive/Profitability Boundary", ["Predictive usefulness and profitability remain not accepted."]),
        ("Runtime Boundary", ["Runtime, strategy, paper trading, and broker execution remain `NOT_AUTHORIZED`."]),
        ("Approval Checklist Summary", [f"Total/passed/failed/blockers: `{validation['total_checks']} / {validation['passed_checks']} / {validation['failed_checks']} / {validation['blocker_count']}`."]),
        ("Remaining Required Tasks", [f"`{gate}`" for gate in approved_artifact["next_gates"]]),
        ("Guardrails", ["No provider request, acquisition, dataset regeneration, predictive acceptance, experiment execution, runtime activation, or trading action occurred."]),
    ]
    lines = ["# MarketFlow Research Registry Approval v1", "", "## Title", "", "- Research Registry Approval v1.", ""]
    for title, body in sections:
        lines.extend([f"## {title}", "", *[f"- {item}" for item in body], ""])
    return "\n".join(lines)


def write_research_registry_approved_v1(
    output_dir: str | Path,
    *,
    research_registry_candidate_review_package: dict[str, Any] | None = None,
    operator_attestation: dict[str, Any],
) -> dict[str, Any]:
    """Write canonical approval JSON without overwriting an existing artifact."""
    artifact = build_research_registry_approved_v1(
        research_registry_candidate_review_package=(
            research_registry_candidate_review_package
        ),
        operator_attestation=operator_attestation,
    )
    validation = validate_research_registry_approved_v1(artifact)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "research_registry_approval_v1.json"
    if path.exists():
        raise ResearchRegistryApprovalError("research registry approval output already exists")
    payload = canonical_json_bytes(artifact)
    path.write_bytes(payload)
    return {
        "path": str(path),
        "artifact_kind": artifact["artifact_kind"],
        "approval_status": artifact["approval_status"],
        "approval_scope": artifact["approval_scope"],
        "research_registry_approval_digest": validation[
            "research_registry_approval_digest"
        ],
        "payload_sha256": sha256_bytes(payload),
    }
