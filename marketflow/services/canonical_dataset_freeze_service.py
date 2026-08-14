"""Guarded offline operator ceremony for the expanded-universe canonical dataset."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import canonical_dataset_results_review_service as review


ARTIFACT_KIND_CANONICAL_DATASET_FROZEN = "CANONICAL_DATASET_FROZEN"
SCHEMA_VERSION_CANONICAL_DATASET_FREEZE_V1 = "canonical_dataset_freeze_v1"
CANONICAL_DATASET_FROZEN = "CANONICAL_DATASET_FROZEN"
CANONICAL_DATASET_FREEZE_ONLY = "CANONICAL_DATASET_FREEZE_ONLY"
OPERATOR_DECISION_FREEZE_CANONICAL_DATASET = "FREEZE_CANONICAL_DATASET"
OPERATOR_ATTESTATION_VERSION_CANONICAL_DATASET_FREEZE_V1 = (
    "canonical_dataset_freeze_operator_attestation_v1"
)
REQUIRED_CANONICAL_DATASET_FREEZE_ATTESTATION_PHRASE = (
    "FREEZE CANONICAL DATASET MSFT NVDA AMZN GOOGL META TSLA JPM XOM "
    "JNJ WMT CAT LMT CANONICAL_DATASET_FREEZE_ONLY"
)

EXPECTED_CANONICAL_DATASET_RESULTS_REVIEW_PACKAGE_DIGEST = (
    "b2815bf7e1fa26db6e852bc04148659cabfd96a58232982245ec291dcac5d37d"
)
EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST = review.EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST
EXPECTED_CANONICAL_DATASET_GENERATION_APPROVAL_DIGEST = (
    review.EXPECTED_CANONICAL_DATASET_GENERATION_APPROVAL_DIGEST
)
EXPECTED_ACQUISITION_GENERATION_FREEZE_DIGEST = (
    review.generation.approval_service.EXPECTED_ACQUISITION_GENERATION_FREEZE_DIGEST
)
EXPECTED_ACQUISITION_GENERATION_APPROVAL_DIGEST = (
    review.generation.approval_service.EXPECTED_ACQUISITION_GENERATION_APPROVAL_DIGEST
)
EXPECTED_ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST = (
    review.generation.approval_service.EXPECTED_ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST
)
EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_EXECUTION_DIGEST = (
    review.generation.approval_service.EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_EXECUTION_DIGEST
)
EXPECTED_CANONICAL_DATASET_CHAIN_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    review.generation.approval_service.EXPECTED_CANONICAL_DATASET_CHAIN_CANDIDATE_REVIEW_PACKAGE_DIGEST
)
EXPECTED_CANONICAL_DATASET_CHAIN_CANDIDATE_DIGEST = (
    review.generation.approval_service.EXPECTED_CANONICAL_DATASET_CHAIN_CANDIDATE_DIGEST
)
EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST = (
    review.generation.approval_service.EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST
)
EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST = (
    review.generation.approval_service.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST
)
EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST = (
    review.generation.approval_service.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST
)
EXPECTED_RECORDS_DIGEST = review.EXPECTED_CANONICAL_RECORDS_SHA256
TARGET_UNIVERSE = list(review.EXPECTED_TARGET_UNIVERSE)
SOURCE_PROFILE = deepcopy(review.EXPECTED_SOURCE_PROFILE)
EXPECTED_RECORD_COUNTS = dict(review.EXPECTED_RECORD_COUNTS)
SOURCE_EVIDENCE_SCOPE = review.SOURCE_EVIDENCE_SCOPE
DATASET_SCOPE = review.DATASET_SCOPE
NOT_AUTHORIZED = review.NOT_AUTHORIZED
NOT_ACCEPTED = review.NOT_ACCEPTED
PASS = review.PASS
FAIL = review.FAIL
BLOCKER = review.BLOCKER

FROZEN_WITH_STANDARD_RECORD_COUNT = "CANONICAL_DATASET_FROZEN"
FROZEN_WITH_REDUCED_RECORD_COUNT_PRESERVED = (
    "CANONICAL_DATASET_FROZEN_WITH_REDUCED_RECORD_COUNT_PRESERVED"
)

REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS = [
    "operator_confirms_source_profile",
    "operator_confirms_meta_reduced_record_count_preserved",
    "operator_confirms_freeze_scope_canonical_dataset_only",
    "operator_confirms_canonical_dataset_generated",
    "operator_confirms_canonical_dataset_freeze",
    "operator_confirms_ready_for_research_registry_candidate",
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
LIMITATIONS = [
    "canonical_dataset_frozen_research_only",
    "registry_approval_not_created",
    "runtime_not_authorized",
    "strategy_use_not_authorized",
    "meta_reduced_record_count_preserved",
    "no_missing_bar_fabrication",
    "no_calendar_session_inference",
    "no_predictive_usefulness_acceptance",
    "no_profitability_acceptance",
    "operator_approval_required_before_research_registry_approval",
]
NEXT_GATES = [
    "research_registry_candidate",
    "research_registry_operator_review",
    "research_registry_approval",
    "additional_predictive_evidence_chain_if_required",
    "runtime_migration_chain_if_ever_authorized",
]
REQUIRED_CHECK_IDS = [
    "canonical_dataset_results_review_digest_matches_expected",
    "canonical_dataset_results_review_has_zero_blockers",
    "canonical_dataset_generation_digest_bound",
    "canonical_dataset_generation_approval_digest_bound",
    "acquisition_generation_freeze_digest_bound",
    "corporate_action_authority_approval_digest_bound",
    "identity_freeze_digest_bound",
    "target_universe_count_12",
    "target_universe_matches_canonical_dataset_results_universe",
    "operator_decision_freeze",
    "operator_attestation_phrase_matches",
    "operator_confirms_all_source_digests",
    "operator_confirms_source_profile",
    "operator_confirms_total_canonical_record_count_11946",
    "operator_confirms_records_digest",
    "operator_confirms_meta_reduced_record_count_preserved",
    "freeze_scope_canonical_dataset_only",
    "canonical_dataset_generated_true",
    "canonical_dataset_frozen_true",
    "ready_for_research_registry_candidate_true",
    "per_ticker_frozen_dataset_entries_12",
    "meta_913_record_count_frozen",
    "non_meta_1003_record_counts_frozen",
    "registry_approval_created_false",
    "additional_predictive_evidence_execution_authorized_false",
    "additional_predictive_evidence_executed_false",
    "predictive_experiment_rerun_authorized_false",
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
    "provider_requests_made_in_freeze_false",
    "live_provider_transport_enabled_in_freeze_false",
    "market_data_acquisition_performed_in_freeze_false",
    "dataset_generation_performed_in_freeze_false",
    "canonical_dataset_regenerated_in_freeze_false",
    "raw_provider_payloads_not_committed",
    "api_keys_not_stored_or_printed",
    "freeze_creates_registry_approval_false",
    "freeze_creates_predictive_evidence_authority_false",
    "freeze_creates_runtime_authority_false",
    "limitations_recorded",
    "next_gates_defined",
    "no_registry_approval_created",
    "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created",
    "no_runtime_migration_approval_created",
]


class CanonicalDatasetFreezeError(ValueError):
    """Raised when freeze evidence, attestation, or an authority boundary is invalid."""


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise CanonicalDatasetFreezeError(f"{field} mismatch")


def _expect_true(actual: Any, field: str) -> None:
    if actual is not True:
        raise CanonicalDatasetFreezeError(f"{field} must be true")


def _expect_false(actual: Any, field: str) -> None:
    if actual is not False:
        raise CanonicalDatasetFreezeError(f"{field} must be false")


def _expect_digest(actual: Any, field: str) -> None:
    if not isinstance(actual, str) or len(actual) != 64:
        raise CanonicalDatasetFreezeError(f"{field} missing")


def build_canonical_dataset_freeze_attestation_v1(
    *,
    operator_reference: str,
    operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str,
    operator_confirms_canonical_dataset_results_review_digest: str,
    operator_confirms_canonical_dataset_generation_digest: str,
    operator_confirms_canonical_dataset_generation_approval_digest: str,
    operator_confirms_acquisition_generation_freeze_digest: str,
    operator_confirms_corporate_action_authority_approval_digest: str,
    operator_confirms_identity_freeze_digest: str,
    operator_confirms_target_universe: list[str],
    operator_confirms_target_count: int,
    operator_confirms_source_profile: bool,
    operator_confirms_total_canonical_record_count: int,
    operator_confirms_records_digest: str,
    operator_confirms_meta_reduced_record_count_preserved: bool,
    operator_confirms_freeze_scope_canonical_dataset_only: bool,
    operator_confirms_canonical_dataset_generated: bool,
    operator_confirms_canonical_dataset_freeze: bool,
    operator_confirms_ready_for_research_registry_candidate: bool,
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
    operator_decision: str = OPERATOR_DECISION_FREEZE_CANONICAL_DATASET,
) -> dict[str, Any]:
    """Build a non-secret attestation; exact validation occurs at freeze."""
    return {name: deepcopy(value) for name, value in locals().items()} | {
        "operator_attestation_version": OPERATOR_ATTESTATION_VERSION_CANONICAL_DATASET_FREEZE_V1
    }


def _expected_digest_confirmations() -> dict[str, str]:
    return {
        "operator_confirms_canonical_dataset_results_review_digest": EXPECTED_CANONICAL_DATASET_RESULTS_REVIEW_PACKAGE_DIGEST,
        "operator_confirms_canonical_dataset_generation_digest": EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST,
        "operator_confirms_canonical_dataset_generation_approval_digest": EXPECTED_CANONICAL_DATASET_GENERATION_APPROVAL_DIGEST,
        "operator_confirms_acquisition_generation_freeze_digest": EXPECTED_ACQUISITION_GENERATION_FREEZE_DIGEST,
        "operator_confirms_corporate_action_authority_approval_digest": EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST,
        "operator_confirms_identity_freeze_digest": EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
    }


def _validate_attestation(attestation: Mapping[str, Any]) -> None:
    if not isinstance(attestation, Mapping):
        raise CanonicalDatasetFreezeError("operator_attestation missing")
    expected = {
        "operator_decision": OPERATOR_DECISION_FREEZE_CANONICAL_DATASET,
        "operator_attestation_phrase": REQUIRED_CANONICAL_DATASET_FREEZE_ATTESTATION_PHRASE,
        "operator_attestation_version": OPERATOR_ATTESTATION_VERSION_CANONICAL_DATASET_FREEZE_V1,
        "operator_confirms_target_universe": TARGET_UNIVERSE,
        "operator_confirms_target_count": 12,
        "operator_confirms_total_canonical_record_count": 11946,
        "operator_confirms_records_digest": EXPECTED_RECORDS_DIGEST,
        **_expected_digest_confirmations(),
    }
    for field, value in expected.items():
        _expect(attestation.get(field), value, field)
    for field in REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS:
        _expect_true(attestation.get(field), field)
    for field in ("operator_reference", "operator_attestation_timestamp_utc"):
        if not isinstance(attestation.get(field), str) or not attestation[field].strip():
            raise CanonicalDatasetFreezeError(f"{field} required")


def _source_review(package: dict[str, Any] | None) -> dict[str, Any]:
    source = (
        review.build_canonical_dataset_results_review_package_v1()
        if package is None
        else deepcopy(package)
    )
    try:
        validation = review.validate_canonical_dataset_results_review_package_v1(source)
    except review.CanonicalDatasetResultsReviewError as exc:
        raise CanonicalDatasetFreezeError("canonical dataset results review invalid") from exc
    _expect(validation.get("status"), review.CANONICAL_DATASET_RESULTS_REVIEW_PACKAGE_READY, "source review status")
    _expect(
        source.get("canonical_dataset_results_review_package_digest"),
        EXPECTED_CANONICAL_DATASET_RESULTS_REVIEW_PACKAGE_DIGEST,
        "source results review digest",
    )
    _expect(source.get("review_summary", {}).get("blocker_count"), 0, "source review blocker count")
    _expect_true(source.get("ready_for_canonical_dataset_freeze"), "source ready_for_canonical_dataset_freeze")
    return source


def per_ticker_canonical_dataset_freeze_digest_v1(entry: dict[str, Any]) -> str:
    payload = deepcopy(entry)
    payload.pop("per_ticker_canonical_dataset_freeze_digest", None)
    return semantic_digest(payload)


def _per_ticker_frozen_entries(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    counts = source["per_ticker_record_counts"]
    for ticker in TARGET_UNIVERSE:
        entry = {
            "ticker": ticker,
            "canonical_dataset_freeze_status": (
                FROZEN_WITH_REDUCED_RECORD_COUNT_PRESERVED
                if ticker == "META"
                else FROZEN_WITH_STANDARD_RECORD_COUNT
            ),
            "canonical_record_count": counts[ticker],
            "meta_reduced_record_count_preserved": ticker == "META",
            "records_digest": source["records_digest"],
            "canonical_dataset_frozen": True,
            "registry_approval_created": False,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
        }
        entry["per_ticker_canonical_dataset_freeze_digest"] = (
            per_ticker_canonical_dataset_freeze_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _base_artifact(source: Mapping[str, Any], attestation: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_CANONICAL_DATASET_FROZEN,
        "schema_version": SCHEMA_VERSION_CANONICAL_DATASET_FREEZE_V1,
        "freeze_status": CANONICAL_DATASET_FROZEN,
        "freeze_scope": CANONICAL_DATASET_FREEZE_ONLY,
        "canonical_dataset_freeze_scope": CANONICAL_DATASET_FREEZE_ONLY,
        "created_offline": True,
        "provider_requests_made_in_freeze": False,
        "live_provider_transport_enabled_in_freeze": False,
        "market_data_acquisition_performed_in_freeze": False,
        "dataset_generation_performed_in_freeze": False,
        "canonical_dataset_regenerated_in_freeze": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "dataset_generation_authorized": True,
        "canonical_dataset_authorized": True,
        "canonical_dataset_generation_approved": True,
        "canonical_dataset_candidate_created": True,
        "canonical_dataset_generation_executed": True,
        "canonical_dataset_generated": True,
        "canonical_dataset_generation_results_created": True,
        "canonical_dataset_results_review_created": True,
        "canonical_dataset_results_review_ready": True,
        "ready_for_canonical_dataset_freeze": True,
        "canonical_dataset_frozen": True,
        "ready_for_research_registry_candidate": True,
        "registry_approval_created": False,
        "canonical_dataset_chain_candidate_created": True,
        "canonical_dataset_chain_candidate_review_created": True,
        "new_ticker_acquisition_authorized": True,
        "acquisition_generation_authorized": True,
        "acquisition_generation_approved": True,
        "acquisition_generation_frozen": True,
        "corporate_action_authority_created": True,
        "corporate_action_authority_approved": True,
        "corporate_action_authority_scope": "CORPORATE_ACTION_AUTHORITY_ONLY",
        "split_event_authority_created": True,
        "split_event_authority_frozen": True,
        "split_event_authority_scope": "SPLIT_EVENT_AUTHORITY_ONLY",
        "dividend_event_authority_created": True,
        "dividend_event_authority_frozen": True,
        "dividend_event_authority_scope": "DIVIDEND_EVENT_AUTHORITY_ONLY",
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
        "canonical_dataset_results_review_package_digest": EXPECTED_CANONICAL_DATASET_RESULTS_REVIEW_PACKAGE_DIGEST,
        "canonical_dataset_generation_digest": EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST,
        "canonical_dataset_generation_approval_digest": EXPECTED_CANONICAL_DATASET_GENERATION_APPROVAL_DIGEST,
        "canonical_dataset_chain_candidate_review_package_digest": EXPECTED_CANONICAL_DATASET_CHAIN_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "canonical_dataset_chain_candidate_digest": EXPECTED_CANONICAL_DATASET_CHAIN_CANDIDATE_DIGEST,
        "acquisition_generation_freeze_digest": EXPECTED_ACQUISITION_GENERATION_FREEZE_DIGEST,
        "acquisition_generation_approval_digest": EXPECTED_ACQUISITION_GENERATION_APPROVAL_DIGEST,
        "acquisition_evidence_results_review_package_digest": EXPECTED_ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        "acquisition_provider_evidence_execution_digest": EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "corporate_action_authority_approval_digest": EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST,
        "identity_authority_freeze_digest": EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
        "ticker_universe_selection_approval_digest": EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST,
        "target_universe": list(TARGET_UNIVERSE),
        "target_universe_count": 12,
        "date_range_start": SOURCE_PROFILE["date_range_start"],
        "date_range_end": SOURCE_PROFILE["date_range_end"],
        "timeframe": SOURCE_PROFILE["timeframe"],
        "profile": SOURCE_PROFILE["profile"],
        "source_profile": deepcopy(SOURCE_PROFILE),
        "source_evidence_scope": SOURCE_EVIDENCE_SCOPE,
        "dataset_scope": DATASET_SCOPE,
        "generated_output_count": 9,
        "total_canonical_record_count": 11946,
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "data_quality_status": "PASS_WITH_PRESERVED_SOURCE_LIMITATION",
        "failure_count": 0,
        "warning_count": 1,
        "per_ticker_record_counts": deepcopy(EXPECTED_RECORD_COUNTS),
        "per_ticker_frozen_canonical_datasets": _per_ticker_frozen_entries(source),
        "canonical_dataset_frozen_by_operator": True,
        "canonical_dataset_freeze_creates_registry_approval": False,
        "canonical_dataset_freeze_creates_predictive_evidence_authority": False,
        "canonical_dataset_freeze_creates_runtime_authority": False,
        "operator_attestation": deepcopy(dict(attestation)),
        "limitations": list(LIMITATIONS),
        "next_gates": list(NEXT_GATES),
        "registry_approval_artifact_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
    }


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if actual == expected else FAIL
    return {
        "check_id": check_id,
        "status": status,
        "expected": expected,
        "actual": actual,
        "severity": BLOCKER,
        "message": "freeze evidence matches" if status == PASS else "freeze evidence mismatch",
    }


def _checklist(artifact: dict[str, Any]) -> list[dict[str, Any]]:
    entries = artifact.get("per_ticker_frozen_canonical_datasets", [])
    counts = artifact.get("per_ticker_record_counts", {})
    attestation = artifact.get("operator_attestation", {})
    digest_confirmations_match = all(
        attestation.get(field) == expected
        for field, expected in _expected_digest_confirmations().items()
    )
    values = {
        "canonical_dataset_results_review_digest_matches_expected": (EXPECTED_CANONICAL_DATASET_RESULTS_REVIEW_PACKAGE_DIGEST, artifact.get("canonical_dataset_results_review_package_digest")),
        "canonical_dataset_results_review_has_zero_blockers": (0, artifact.get("source_results_review_blocker_count")),
        "canonical_dataset_generation_digest_bound": (EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST, artifact.get("canonical_dataset_generation_digest")),
        "canonical_dataset_generation_approval_digest_bound": (EXPECTED_CANONICAL_DATASET_GENERATION_APPROVAL_DIGEST, artifact.get("canonical_dataset_generation_approval_digest")),
        "acquisition_generation_freeze_digest_bound": (EXPECTED_ACQUISITION_GENERATION_FREEZE_DIGEST, artifact.get("acquisition_generation_freeze_digest")),
        "corporate_action_authority_approval_digest_bound": (EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST, artifact.get("corporate_action_authority_approval_digest")),
        "identity_freeze_digest_bound": (EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST, artifact.get("identity_authority_freeze_digest")),
        "target_universe_count_12": (12, artifact.get("target_universe_count")),
        "target_universe_matches_canonical_dataset_results_universe": (TARGET_UNIVERSE, artifact.get("target_universe")),
        "operator_decision_freeze": (OPERATOR_DECISION_FREEZE_CANONICAL_DATASET, attestation.get("operator_decision")),
        "operator_attestation_phrase_matches": (REQUIRED_CANONICAL_DATASET_FREEZE_ATTESTATION_PHRASE, attestation.get("operator_attestation_phrase")),
        "operator_confirms_all_source_digests": (True, digest_confirmations_match),
        "operator_confirms_source_profile": (True, attestation.get("operator_confirms_source_profile")),
        "operator_confirms_total_canonical_record_count_11946": (11946, attestation.get("operator_confirms_total_canonical_record_count")),
        "operator_confirms_records_digest": (EXPECTED_RECORDS_DIGEST, attestation.get("operator_confirms_records_digest")),
        "operator_confirms_meta_reduced_record_count_preserved": (True, attestation.get("operator_confirms_meta_reduced_record_count_preserved")),
        "freeze_scope_canonical_dataset_only": (CANONICAL_DATASET_FREEZE_ONLY, artifact.get("freeze_scope")),
        "canonical_dataset_generated_true": (True, artifact.get("canonical_dataset_generated")),
        "canonical_dataset_frozen_true": (True, artifact.get("canonical_dataset_frozen")),
        "ready_for_research_registry_candidate_true": (True, artifact.get("ready_for_research_registry_candidate")),
        "per_ticker_frozen_dataset_entries_12": (12, len(entries)),
        "meta_913_record_count_frozen": (913, counts.get("META")),
        "non_meta_1003_record_counts_frozen": (True, bool(counts) and all(count == 1003 for ticker, count in counts.items() if ticker != "META")),
        "registry_approval_created_false": (False, artifact.get("registry_approval_created")),
        "additional_predictive_evidence_execution_authorized_false": (False, artifact.get("additional_predictive_evidence_execution_authorized")),
        "additional_predictive_evidence_executed_false": (False, artifact.get("additional_predictive_evidence_executed")),
        "predictive_experiment_rerun_authorized_false": (False, artifact.get("predictive_experiment_rerun_authorized")),
        "feature_matrix_regeneration_performed_false": (False, artifact.get("feature_matrix_regeneration_performed")),
        "new_strategy_scoring_performed_false": (False, artifact.get("new_strategy_scoring_performed")),
        "trade_recommendations_generated_false": (False, artifact.get("trade_recommendations_generated")),
        "predictive_usefulness_not_accepted": (NOT_ACCEPTED, artifact.get("predictive_usefulness")),
        "profitability_not_accepted": (NOT_ACCEPTED, artifact.get("profitability")),
        "runtime_migration_approved_false": (False, artifact.get("runtime_migration_approved")),
        "runtime_use_not_authorized": (NOT_AUTHORIZED, artifact.get("runtime_use")),
        "strategy_use_not_authorized": (NOT_AUTHORIZED, artifact.get("strategy_use")),
        "paper_trading_not_authorized": (NOT_AUTHORIZED, artifact.get("paper_trading")),
        "broker_execution_not_authorized": (NOT_AUTHORIZED, artifact.get("broker_execution")),
        "automatic_stitching_false": (False, artifact.get("automatic_stitching")),
        "provider_requests_made_in_freeze_false": (False, artifact.get("provider_requests_made_in_freeze")),
        "live_provider_transport_enabled_in_freeze_false": (False, artifact.get("live_provider_transport_enabled_in_freeze")),
        "market_data_acquisition_performed_in_freeze_false": (False, artifact.get("market_data_acquisition_performed_in_freeze")),
        "dataset_generation_performed_in_freeze_false": (False, artifact.get("dataset_generation_performed_in_freeze")),
        "canonical_dataset_regenerated_in_freeze_false": (False, artifact.get("canonical_dataset_regenerated_in_freeze")),
        "raw_provider_payloads_not_committed": (False, artifact.get("raw_provider_payloads_committed")),
        "api_keys_not_stored_or_printed": (False, artifact.get("api_keys_stored_or_printed")),
        "freeze_creates_registry_approval_false": (False, artifact.get("canonical_dataset_freeze_creates_registry_approval")),
        "freeze_creates_predictive_evidence_authority_false": (False, artifact.get("canonical_dataset_freeze_creates_predictive_evidence_authority")),
        "freeze_creates_runtime_authority_false": (False, artifact.get("canonical_dataset_freeze_creates_runtime_authority")),
        "limitations_recorded": (LIMITATIONS, artifact.get("limitations")),
        "next_gates_defined": (NEXT_GATES, artifact.get("next_gates")),
        "no_registry_approval_created": (False, artifact.get("registry_approval_artifact_created")),
        "no_predictive_usefulness_acceptance_artifact_created": (False, artifact.get("predictive_usefulness_acceptance_artifact_created")),
        "no_profitability_acceptance_created": (False, artifact.get("profitability_acceptance_created")),
        "no_runtime_migration_approval_created": (False, artifact.get("runtime_migration_approval_created")),
    }
    return [_check(check_id, *values[check_id]) for check_id in REQUIRED_CHECK_IDS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [row for row in checklist if row.get("status") != PASS]
    return {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row.get("severity") == BLOCKER for row in failed),
        "canonical_dataset_frozen_by_operator": not failed,
        "freeze_scope": CANONICAL_DATASET_FREEZE_ONLY,
        "canonical_dataset_generated": True,
        "canonical_dataset_frozen": not failed,
        "ready_for_research_registry_candidate": not failed,
        "registry_approval_created": False,
        "additional_predictive_evidence_execution_authorized": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def canonical_dataset_freeze_digest_v1(artifact: dict[str, Any]) -> str:
    payload = deepcopy(artifact)
    payload.pop("canonical_dataset_freeze_digest", None)
    return semantic_digest(payload)


def build_canonical_dataset_frozen_v1(
    *, canonical_dataset_results_review_package: dict[str, Any] | None = None,
    operator_attestation: dict[str, Any],
) -> dict[str, Any]:
    """Freeze the reviewed dataset only after exact non-secret operator attestation."""
    source = _source_review(canonical_dataset_results_review_package)
    _validate_attestation(operator_attestation)
    artifact = _base_artifact(source, operator_attestation)
    artifact["source_results_review_blocker_count"] = source["review_summary"]["blocker_count"]
    artifact["freeze_checklist"] = _checklist(artifact)
    artifact["freeze_summary"] = _summary(artifact["freeze_checklist"])
    artifact["canonical_dataset_freeze_digest"] = canonical_dataset_freeze_digest_v1(artifact)
    validate_canonical_dataset_frozen_v1(artifact)
    return artifact


def _validate_per_ticker(artifact: dict[str, Any]) -> None:
    entries = artifact.get("per_ticker_frozen_canonical_datasets")
    if not isinstance(entries, list) or len(entries) != 12:
        raise CanonicalDatasetFreezeError("per-ticker frozen dataset entries mismatch")
    _expect([row.get("ticker") for row in entries], TARGET_UNIVERSE, "per-ticker frozen dataset order")
    for row in entries:
        ticker = row["ticker"]
        expected = {
            "canonical_dataset_freeze_status": (
                FROZEN_WITH_REDUCED_RECORD_COUNT_PRESERVED
                if ticker == "META"
                else FROZEN_WITH_STANDARD_RECORD_COUNT
            ),
            "canonical_record_count": EXPECTED_RECORD_COUNTS[ticker],
            "meta_reduced_record_count_preserved": ticker == "META",
            "records_digest": EXPECTED_RECORDS_DIGEST,
            "canonical_dataset_frozen": True,
            "registry_approval_created": False,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
        }
        for field, value in expected.items():
            _expect(row.get(field), value, f"{ticker}.{field}")
        digest = row.get("per_ticker_canonical_dataset_freeze_digest")
        _expect_digest(digest, f"{ticker}.per_ticker_canonical_dataset_freeze_digest")
        _expect(digest, per_ticker_canonical_dataset_freeze_digest_v1(row), f"{ticker}.freeze digest")


def validate_canonical_dataset_frozen_v1(frozen_artifact: dict[str, Any]) -> dict[str, Any]:
    """Validate the exact attestation, source bindings, freeze, and closed downstream gates."""
    if not isinstance(frozen_artifact, dict):
        raise CanonicalDatasetFreezeError("frozen_artifact must be an object")
    expected = {
        "artifact_kind": ARTIFACT_KIND_CANONICAL_DATASET_FROZEN,
        "schema_version": SCHEMA_VERSION_CANONICAL_DATASET_FREEZE_V1,
        "freeze_status": CANONICAL_DATASET_FROZEN,
        "freeze_scope": CANONICAL_DATASET_FREEZE_ONLY,
        "canonical_dataset_freeze_scope": CANONICAL_DATASET_FREEZE_ONLY,
        "canonical_dataset_results_review_package_digest": EXPECTED_CANONICAL_DATASET_RESULTS_REVIEW_PACKAGE_DIGEST,
        "canonical_dataset_generation_digest": EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST,
        "canonical_dataset_generation_approval_digest": EXPECTED_CANONICAL_DATASET_GENERATION_APPROVAL_DIGEST,
        "canonical_dataset_chain_candidate_review_package_digest": EXPECTED_CANONICAL_DATASET_CHAIN_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "canonical_dataset_chain_candidate_digest": EXPECTED_CANONICAL_DATASET_CHAIN_CANDIDATE_DIGEST,
        "acquisition_generation_freeze_digest": EXPECTED_ACQUISITION_GENERATION_FREEZE_DIGEST,
        "acquisition_generation_approval_digest": EXPECTED_ACQUISITION_GENERATION_APPROVAL_DIGEST,
        "acquisition_evidence_results_review_package_digest": EXPECTED_ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        "acquisition_provider_evidence_execution_digest": EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "corporate_action_authority_approval_digest": EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST,
        "identity_authority_freeze_digest": EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
        "ticker_universe_selection_approval_digest": EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST,
        "target_universe": TARGET_UNIVERSE,
        "target_universe_count": 12,
        "date_range_start": SOURCE_PROFILE["date_range_start"],
        "date_range_end": SOURCE_PROFILE["date_range_end"],
        "timeframe": SOURCE_PROFILE["timeframe"],
        "profile": SOURCE_PROFILE["profile"],
        "source_profile": SOURCE_PROFILE,
        "source_evidence_scope": SOURCE_EVIDENCE_SCOPE,
        "dataset_scope": DATASET_SCOPE,
        "generated_output_count": 9,
        "total_canonical_record_count": 11946,
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "per_ticker_record_counts": EXPECTED_RECORD_COUNTS,
        "data_quality_status": "PASS_WITH_PRESERVED_SOURCE_LIMITATION",
        "failure_count": 0,
        "warning_count": 1,
        "source_results_review_blocker_count": 0,
        "corporate_action_authority_scope": "CORPORATE_ACTION_AUTHORITY_ONLY",
        "split_event_authority_scope": "SPLIT_EVENT_AUTHORITY_ONLY",
        "dividend_event_authority_scope": "DIVIDEND_EVENT_AUTHORITY_ONLY",
        "limitations": LIMITATIONS,
        "next_gates": NEXT_GATES,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
    }
    for field, value in expected.items():
        _expect(frozen_artifact.get(field), value, field)
    for field in (
        "created_offline", "dataset_generation_authorized", "canonical_dataset_authorized",
        "canonical_dataset_generation_approved", "canonical_dataset_candidate_created",
        "canonical_dataset_generation_executed", "canonical_dataset_generated",
        "canonical_dataset_generation_results_created", "canonical_dataset_results_review_created",
        "canonical_dataset_results_review_ready", "ready_for_canonical_dataset_freeze",
        "canonical_dataset_frozen", "ready_for_research_registry_candidate",
        "canonical_dataset_chain_candidate_created", "canonical_dataset_chain_candidate_review_created",
        "new_ticker_acquisition_authorized", "acquisition_generation_authorized",
        "acquisition_generation_approved", "acquisition_generation_frozen",
        "corporate_action_authority_created", "corporate_action_authority_approved",
        "split_event_authority_created", "split_event_authority_frozen",
        "dividend_event_authority_created", "dividend_event_authority_frozen",
        "identity_authority_created", "identity_authority_frozen", "research_only",
        "canonical_dataset_frozen_by_operator",
    ):
        _expect_true(frozen_artifact.get(field), field)
    for field in (
        "provider_requests_made_in_freeze", "live_provider_transport_enabled_in_freeze",
        "market_data_acquisition_performed_in_freeze", "dataset_generation_performed_in_freeze",
        "canonical_dataset_regenerated_in_freeze", "raw_provider_payloads_committed",
        "api_keys_stored_or_printed", "registry_approval_created",
        "additional_predictive_evidence_execution_authorized", "additional_predictive_evidence_executed",
        "predictive_experiment_rerun_authorized", "predictive_experiment_rerun_performed",
        "feature_matrix_regeneration_performed", "new_strategy_scoring_performed",
        "trade_recommendations_generated", "runtime_migration_approved", "runtime_migration_active",
        "automatic_stitching", "canonical_dataset_freeze_creates_registry_approval",
        "canonical_dataset_freeze_creates_predictive_evidence_authority",
        "canonical_dataset_freeze_creates_runtime_authority", "registry_approval_artifact_created",
        "predictive_usefulness_acceptance_artifact_created", "profitability_acceptance_created",
        "runtime_migration_approval_created",
    ):
        _expect_false(frozen_artifact.get(field), field)
    _validate_attestation(frozen_artifact.get("operator_attestation", {}))
    _validate_per_ticker(frozen_artifact)
    checklist = frozen_artifact.get("freeze_checklist")
    if not isinstance(checklist, list):
        raise CanonicalDatasetFreezeError("freeze_checklist missing")
    _expect([row.get("check_id") for row in checklist], REQUIRED_CHECK_IDS, "freeze checklist ids")
    _expect(checklist, _checklist(frozen_artifact), "freeze checklist")
    if any(row.get("status") != PASS or row.get("severity") != BLOCKER for row in checklist):
        raise CanonicalDatasetFreezeError("freeze checklist must pass")
    _expect(frozen_artifact.get("freeze_summary"), _summary(checklist), "freeze_summary")
    digest = frozen_artifact.get("canonical_dataset_freeze_digest")
    _expect_digest(digest, "canonical_dataset_freeze_digest")
    _expect(digest, canonical_dataset_freeze_digest_v1(frozen_artifact), "canonical_dataset_freeze_digest")
    return {
        "status": CANONICAL_DATASET_FROZEN,
        "freeze_scope": CANONICAL_DATASET_FREEZE_ONLY,
        "canonical_dataset_freeze_digest": digest,
        "total_checks": frozen_artifact["freeze_summary"]["total_checks"],
        "passed_checks": frozen_artifact["freeze_summary"]["passed_checks"],
        "failed_checks": frozen_artifact["freeze_summary"]["failed_checks"],
        "blocker_count": frozen_artifact["freeze_summary"]["blocker_count"],
    }


def build_canonical_dataset_frozen_markdown_v1(frozen_artifact: dict[str, Any]) -> str:
    """Render the frozen canonical dataset and its remaining closed gates."""
    validation = validate_canonical_dataset_frozen_v1(frozen_artifact)
    operator = frozen_artifact["operator_attestation"]
    sections = [
        ("Frozen Canonical Dataset", [f"Artifact/status/scope: `{frozen_artifact['artifact_kind']}` / `{validation['status']}` / `{validation['freeze_scope']}`.", f"Freeze digest: `{validation['canonical_dataset_freeze_digest']}`."]),
        ("Operator Attestation", [f"Decision/reference/timestamp: `{operator['operator_decision']}` / `{operator['operator_reference']}` / `{operator['operator_attestation_timestamp_utc']}`."]),
        ("Source Canonical Dataset Results Review", [f"Review digest: `{frozen_artifact['canonical_dataset_results_review_package_digest']}`."]),
        ("Source Canonical Dataset Generation", [f"Generation/approval digests: `{frozen_artifact['canonical_dataset_generation_digest']}` / `{frozen_artifact['canonical_dataset_generation_approval_digest']}`."]),
        ("Target Universe", [", ".join(f"`{ticker}`" for ticker in frozen_artifact["target_universe"]) + "."]),
        ("Source Profile", [f"`{key}`: `{value}`." for key, value in frozen_artifact["source_profile"].items()]),
        ("Frozen Per-Ticker Canonical Dataset Summary", [f"`{row['ticker']}`: `{row['canonical_dataset_freeze_status']}`, `{row['canonical_record_count']}` records." for row in frozen_artifact["per_ticker_frozen_canonical_datasets"]]),
        ("META Reduced Record Count Preservation", ["META is frozen exactly at `913`; no repair, inference, smoothing, or backfill occurred."]),
        ("Records Digest", [f"`{frozen_artifact['records_digest']}`."]),
        ("Freeze Scope", ["`CANONICAL_DATASET_FREEZE_ONLY` freezes the reviewed research dataset and grants no downstream authority."]),
        ("Registry Boundary", ["No registry approval was created."]),
        ("Predictive/Profitability Boundary", ["Predictive usefulness and profitability remain not accepted."]),
        ("Runtime Boundary", ["Runtime, strategy, paper trading, and broker execution remain `NOT_AUTHORIZED`."]),
        ("Freeze Checklist Summary", [f"Total/passed/failed/blockers: `{validation['total_checks']} / {validation['passed_checks']} / {validation['failed_checks']} / {validation['blocker_count']}`."]),
        ("Remaining Required Tasks", [f"`{item}`" for item in frozen_artifact["next_gates"]]),
        ("Guardrails", ["No provider request, acquisition, dataset regeneration, registry approval, predictive acceptance, runtime activation, or trading action occurred."]),
    ]
    lines = ["# MarketFlow Canonical Dataset Freeze v1", "", "## Title", "", "- Canonical Dataset Freeze Ceremony v1.", ""]
    for title, body in sections:
        lines.extend([f"## {title}", "", *[f"- {item}" for item in body], ""])
    return "\n".join(lines)


def write_canonical_dataset_frozen_v1(
    output_dir: str | Path, *,
    canonical_dataset_results_review_package: dict[str, Any] | None = None,
    operator_attestation: dict[str, Any],
) -> dict[str, Any]:
    """Write canonical freeze JSON without overwriting an existing artifact."""
    artifact = build_canonical_dataset_frozen_v1(
        canonical_dataset_results_review_package=canonical_dataset_results_review_package,
        operator_attestation=operator_attestation,
    )
    validation = validate_canonical_dataset_frozen_v1(artifact)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "canonical_dataset_frozen_v1.json"
    if path.exists():
        raise CanonicalDatasetFreezeError("canonical dataset freeze output already exists")
    payload = canonical_json_bytes(artifact)
    path.write_bytes(payload)
    return {
        "path": str(path),
        "artifact_kind": artifact["artifact_kind"],
        "freeze_status": artifact["freeze_status"],
        "freeze_scope": artifact["freeze_scope"],
        "canonical_dataset_freeze_digest": validation["canonical_dataset_freeze_digest"],
        "payload_sha256": sha256_bytes(payload),
    }
