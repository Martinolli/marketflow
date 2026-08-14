"""Offline candidate proposing a frozen canonical dataset for future registry review."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import canonical_dataset_freeze_service as freeze


ARTIFACT_KIND_RESEARCH_REGISTRY_CANDIDATE = "RESEARCH_REGISTRY_CANDIDATE"
SCHEMA_VERSION_RESEARCH_REGISTRY_CANDIDATE_V1 = "research_registry_candidate_v1"
RESEARCH_REGISTRY_READY_FOR_OPERATOR_REVIEW = "RESEARCH_REGISTRY_READY_FOR_OPERATOR_REVIEW"
RESEARCH_REGISTRY_CANDIDATE_OBJECTIVE = (
    "PLAN_RESEARCH_REGISTRY_ADMISSION_FOR_FROZEN_CANONICAL_DATASET_EXPANDED_UNIVERSE"
)
RESEARCH_REGISTRY_CANDIDATE_SCOPE = "REGISTRY_CANDIDATE_ONLY_NOT_APPROVAL"
RESEARCH_REGISTRY_MODE = "PLANNED_NOT_APPROVED"
RESEARCH_REGISTRY_AUTHORITY_STATUS = "NOT_APPROVED"
PLANNED_READY_FOR_OPERATOR_REVIEW = "PLANNED_READY_FOR_OPERATOR_REVIEW"
PLANNED_NOT_GENERATED = "PLANNED_NOT_GENERATED"
RESEARCH_ONLY_NON_ACTIONABLE = "RESEARCH_ONLY_NON_ACTIONABLE"
SOURCE_BINDING_MODE_COMMITTED_STATUS = "COMMITTED_FREEZE_STATUS_DIGEST_BOUND"

EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST = (
    "02af746fa11fa292a84e000ff8ca19a0b4ab36937558f938e4ac04eef6be92fc"
)
EXPECTED_CANONICAL_DATASET_RESULTS_REVIEW_PACKAGE_DIGEST = (
    freeze.EXPECTED_CANONICAL_DATASET_RESULTS_REVIEW_PACKAGE_DIGEST
)
EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST = freeze.EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST
EXPECTED_CANONICAL_DATASET_GENERATION_APPROVAL_DIGEST = (
    freeze.EXPECTED_CANONICAL_DATASET_GENERATION_APPROVAL_DIGEST
)
EXPECTED_CANONICAL_DATASET_CHAIN_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    freeze.EXPECTED_CANONICAL_DATASET_CHAIN_CANDIDATE_REVIEW_PACKAGE_DIGEST
)
EXPECTED_CANONICAL_DATASET_CHAIN_CANDIDATE_DIGEST = (
    freeze.EXPECTED_CANONICAL_DATASET_CHAIN_CANDIDATE_DIGEST
)
EXPECTED_ACQUISITION_GENERATION_FREEZE_DIGEST = freeze.EXPECTED_ACQUISITION_GENERATION_FREEZE_DIGEST
EXPECTED_ACQUISITION_GENERATION_APPROVAL_DIGEST = freeze.EXPECTED_ACQUISITION_GENERATION_APPROVAL_DIGEST
EXPECTED_ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST = (
    freeze.EXPECTED_ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST
)
EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_EXECUTION_DIGEST = (
    freeze.EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_EXECUTION_DIGEST
)
EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST = (
    freeze.EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST
)
EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST = freeze.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST
EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST = (
    freeze.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST
)
EXPECTED_RECORDS_DIGEST = freeze.EXPECTED_RECORDS_DIGEST
TARGET_UNIVERSE = list(freeze.TARGET_UNIVERSE)
SOURCE_PROFILE = deepcopy(freeze.SOURCE_PROFILE)
EXPECTED_RECORD_COUNTS = dict(freeze.EXPECTED_RECORD_COUNTS)
NOT_AUTHORIZED = freeze.NOT_AUTHORIZED
NOT_ACCEPTED = freeze.NOT_ACCEPTED
PASS = freeze.PASS
FAIL = freeze.FAIL
BLOCKER = freeze.BLOCKER

REGISTRY_CANDIDATE_METADATA = {
    "dataset_name": "expanded_universe_canonical_dataset_v1",
    "dataset_scope": freeze.DATASET_SCOPE,
    "source_profile": SOURCE_PROFILE["profile"],
    "date_range_start": SOURCE_PROFILE["date_range_start"],
    "date_range_end": SOURCE_PROFILE["date_range_end"],
    "timeframe": SOURCE_PROFILE["timeframe"],
    "target_universe_count": 12,
    "total_canonical_record_count": 11946,
    "records_digest": EXPECTED_RECORDS_DIGEST,
    "canonical_dataset_freeze_digest": EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST,
    "data_quality_status": "PASS_WITH_PRESERVED_SOURCE_LIMITATION",
    "registry_candidate_label": RESEARCH_ONLY_NON_ACTIONABLE,
}
REGISTRY_PLANNING_DIMENSIONS = [
    "frozen_canonical_dataset_binding",
    "records_digest_binding",
    "source_authority_chain_binding",
    "ticker_universe_binding",
    "dataset_scope_classification",
    "research_only_labeling_policy",
    "data_quality_status_policy",
    "meta_reduced_record_count_policy",
    "source_profile_policy",
    "schema_contract_policy",
    "digest_manifest_policy",
    "access_control_policy",
    "registry_entry_metadata_policy",
    "registry_versioning_policy",
    "registry_approval_gate_policy",
    "predictive_use_boundary_policy",
    "runtime_use_boundary_policy",
]
FUTURE_REGISTRY_CHAIN = [
    "research_registry_candidate_operator_review_package",
    "research_registry_approval_ceremony",
    "research_registry_status_publication",
    "additional_predictive_evidence_planning_if_required",
    "predictive_usefulness_reassessment_if_required",
    "profitability_review_chain_if_required",
    "runtime_migration_chain_if_ever_separately_authorized",
]
FUTURE_GATES = [
    "research_registry_candidate_operator_review",
    "research_registry_approval_ceremony",
    "research_registry_status_publication",
    "additional_predictive_evidence_chain_if_required",
    "predictive_usefulness_reassessment_if_required",
    "profitability_review_chain_if_required",
    "runtime_migration_chain_if_ever_authorized",
]
RISK_CONTROLS = [
    "no_registry_approval_without_operator_approval",
    "no_predictive_use_without_registry_approval",
    "no_runtime_source_switch",
    "no_automatic_stitching",
    "no_broker_execution",
    "no_paper_trading",
    "no_trade_recommendations",
    "no_predictive_usefulness_acceptance",
    "no_profitability_acceptance",
    "preserve_meta_reduced_record_count",
    "do_not_mutate_frozen_canonical_dataset",
    "no_raw_provider_payload_commit",
    "no_api_key_storage_or_printing",
    "all_outputs_labeled_research_only",
]
PLANNED_OUTPUT_NAMES = [
    "research_registry_candidate_manifest",
    "research_registry_entry_template",
    "per_ticker_registry_candidate_summary",
    "registry_source_authority_chain_manifest",
    "registry_digest_manifest_template",
    "operator_review_summary_template",
]
REQUIRED_CHECK_IDS = [
    "canonical_dataset_freeze_digest_bound",
    "canonical_dataset_results_review_digest_bound",
    "canonical_dataset_generation_digest_bound",
    "canonical_dataset_generation_approval_digest_bound",
    "records_digest_bound",
    "identity_freeze_digest_bound",
    "target_universe_count_12",
    "target_universe_matches_frozen_canonical_dataset_universe",
    "canonical_dataset_generated_true",
    "canonical_dataset_frozen_true",
    "ready_for_research_registry_candidate_true",
    "research_registry_candidate_created_true",
    "research_registry_candidate_scope_candidate_only",
    "research_registry_authority_status_not_approved",
    "total_canonical_record_count_11946",
    "meta_record_count_913_preserved",
    "non_meta_record_counts_1003_preserved",
    "registry_metadata_defined",
    "registry_planning_dimensions_defined",
    "future_registry_chain_defined",
    "future_gates_defined",
    "risk_controls_defined",
    "planned_outputs_not_generated",
    "planned_outputs_research_only",
    "provider_requests_made_false",
    "live_provider_transport_enabled_false",
    "market_data_acquisition_performed_false",
    "dataset_generation_performed_false",
    "canonical_dataset_regenerated_false",
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
    "no_registry_approval_artifact_created",
    "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created",
    "no_runtime_migration_approval_created",
]


class ResearchRegistryCandidateError(ValueError):
    """Raised when registry candidate evidence or an authority boundary is invalid."""


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise ResearchRegistryCandidateError(f"{field} mismatch")


def _expect_true(actual: Any, field: str) -> None:
    if actual is not True:
        raise ResearchRegistryCandidateError(f"{field} must be true")


def _expect_false(actual: Any, field: str) -> None:
    if actual is not False:
        raise ResearchRegistryCandidateError(f"{field} must be false")


def _expect_digest(actual: Any, field: str) -> None:
    if not isinstance(actual, str) or len(actual) != 64:
        raise ResearchRegistryCandidateError(f"{field} missing")


def _committed_freeze_binding() -> dict[str, Any]:
    """Return the exact checked-in freeze-status projection without rebuilding it."""
    return {
        "artifact_kind": freeze.ARTIFACT_KIND_CANONICAL_DATASET_FROZEN,
        "freeze_status": freeze.CANONICAL_DATASET_FROZEN,
        "freeze_scope": freeze.CANONICAL_DATASET_FREEZE_ONLY,
        "canonical_dataset_freeze_digest": EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST,
        "canonical_dataset_results_review_package_digest": EXPECTED_CANONICAL_DATASET_RESULTS_REVIEW_PACKAGE_DIGEST,
        "canonical_dataset_generation_digest": EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST,
        "canonical_dataset_generation_approval_digest": EXPECTED_CANONICAL_DATASET_GENERATION_APPROVAL_DIGEST,
        "target_universe": list(TARGET_UNIVERSE),
        "target_universe_count": 12,
        "source_profile": deepcopy(SOURCE_PROFILE),
        "total_canonical_record_count": 11946,
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "per_ticker_record_counts": deepcopy(EXPECTED_RECORD_COUNTS),
        "canonical_dataset_generated": True,
        "canonical_dataset_frozen": True,
        "ready_for_research_registry_candidate": True,
        "freeze_summary": {"blocker_count": 0},
    }


def _source_freeze(source_artifact: dict[str, Any] | None) -> tuple[dict[str, Any], str]:
    if source_artifact is None:
        source = _committed_freeze_binding()
        binding_mode = SOURCE_BINDING_MODE_COMMITTED_STATUS
    else:
        source = deepcopy(source_artifact)
        try:
            freeze.validate_canonical_dataset_frozen_v1(source)
        except freeze.CanonicalDatasetFreezeError as exc:
            raise ResearchRegistryCandidateError("canonical dataset freeze artifact invalid") from exc
        binding_mode = "VALIDATED_FREEZE_ARTIFACT"
    expected = {
        "artifact_kind": freeze.ARTIFACT_KIND_CANONICAL_DATASET_FROZEN,
        "freeze_status": freeze.CANONICAL_DATASET_FROZEN,
        "freeze_scope": freeze.CANONICAL_DATASET_FREEZE_ONLY,
        "canonical_dataset_freeze_digest": EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST,
        "canonical_dataset_results_review_package_digest": EXPECTED_CANONICAL_DATASET_RESULTS_REVIEW_PACKAGE_DIGEST,
        "canonical_dataset_generation_digest": EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST,
        "canonical_dataset_generation_approval_digest": EXPECTED_CANONICAL_DATASET_GENERATION_APPROVAL_DIGEST,
        "target_universe": TARGET_UNIVERSE,
        "target_universe_count": 12,
        "source_profile": SOURCE_PROFILE,
        "total_canonical_record_count": 11946,
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "per_ticker_record_counts": EXPECTED_RECORD_COUNTS,
        "canonical_dataset_generated": True,
        "canonical_dataset_frozen": True,
        "ready_for_research_registry_candidate": True,
    }
    for field, value in expected.items():
        _expect(source.get(field), value, f"source freeze {field}")
    _expect(source.get("freeze_summary", {}).get("blocker_count"), 0, "source freeze blocker count")
    return source, binding_mode


def per_ticker_research_registry_candidate_digest_v1(entry: dict[str, Any]) -> str:
    payload = deepcopy(entry)
    payload.pop("per_ticker_research_registry_candidate_digest", None)
    return semantic_digest(payload)


def _per_ticker_entries(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for ticker in TARGET_UNIVERSE:
        entry = {
            "ticker": ticker,
            "identity_authority_status": "FROZEN",
            "corporate_action_authority_status": "APPROVED",
            "acquisition_generation_status": "FROZEN",
            "canonical_dataset_status": "FROZEN",
            "research_registry_candidate_status": PLANNED_READY_FOR_OPERATOR_REVIEW,
            "historical_record_count": source["per_ticker_record_counts"][ticker],
            "meta_reduced_record_count_flag": ticker == "META",
            "registry_approval_created": False,
            "predictive_usefulness": NOT_ACCEPTED,
            "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
        }
        entry["per_ticker_research_registry_candidate_digest"] = (
            per_ticker_research_registry_candidate_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _planned_outputs() -> list[dict[str, Any]]:
    return [
        {
            "planned_output": name,
            "generation_status": PLANNED_NOT_GENERATED,
            "output_label": RESEARCH_ONLY_NON_ACTIONABLE,
        }
        for name in PLANNED_OUTPUT_NAMES
    ]


def _base_candidate(source: Mapping[str, Any], binding_mode: str) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_RESEARCH_REGISTRY_CANDIDATE,
        "schema_version": SCHEMA_VERSION_RESEARCH_REGISTRY_CANDIDATE_V1,
        "candidate_status": RESEARCH_REGISTRY_READY_FOR_OPERATOR_REVIEW,
        "created_offline": True,
        "provider_requests_made": False,
        "live_provider_transport_enabled": False,
        "market_data_acquisition_performed": False,
        "dataset_generation_performed": False,
        "canonical_dataset_regenerated": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "research_registry_candidate_created": True,
        "research_registry_candidate_ready_for_operator_review": True,
        "research_registry_approved": False,
        "registry_approval_created": False,
        "canonical_dataset_generated": True,
        "canonical_dataset_frozen": True,
        "canonical_dataset_freeze_scope": freeze.CANONICAL_DATASET_FREEZE_ONLY,
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
        "operator_review_required": True,
        "canonical_dataset_freeze_digest": EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST,
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
        "source_freeze_binding_mode": binding_mode,
        "source_freeze_blocker_count": source["freeze_summary"]["blocker_count"],
        "target_universe": list(TARGET_UNIVERSE),
        "target_universe_count": 12,
        "source_profile": deepcopy(SOURCE_PROFILE),
        "total_canonical_record_count": 11946,
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "per_ticker_record_counts": deepcopy(EXPECTED_RECORD_COUNTS),
        "data_quality_status": "PASS_WITH_PRESERVED_SOURCE_LIMITATION",
        "research_registry_candidate_objective": RESEARCH_REGISTRY_CANDIDATE_OBJECTIVE,
        "research_registry_candidate_scope": RESEARCH_REGISTRY_CANDIDATE_SCOPE,
        "research_registry_mode": RESEARCH_REGISTRY_MODE,
        "research_registry_authority_status": RESEARCH_REGISTRY_AUTHORITY_STATUS,
        "registry_candidate_metadata": deepcopy(REGISTRY_CANDIDATE_METADATA),
        "registry_planning_dimensions": list(REGISTRY_PLANNING_DIMENSIONS),
        "per_ticker_research_registry_candidates": _per_ticker_entries(source),
        "future_registry_chain": list(FUTURE_REGISTRY_CHAIN),
        "future_gates": list(FUTURE_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "planned_outputs": _planned_outputs(),
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
        "message": "candidate evidence matches" if status == PASS else "candidate evidence mismatch",
    }


def _checklist(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    counts = candidate.get("per_ticker_record_counts", {})
    planned = candidate.get("planned_outputs", [])
    values = {
        "canonical_dataset_freeze_digest_bound": (EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST, candidate.get("canonical_dataset_freeze_digest")),
        "canonical_dataset_results_review_digest_bound": (EXPECTED_CANONICAL_DATASET_RESULTS_REVIEW_PACKAGE_DIGEST, candidate.get("canonical_dataset_results_review_package_digest")),
        "canonical_dataset_generation_digest_bound": (EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST, candidate.get("canonical_dataset_generation_digest")),
        "canonical_dataset_generation_approval_digest_bound": (EXPECTED_CANONICAL_DATASET_GENERATION_APPROVAL_DIGEST, candidate.get("canonical_dataset_generation_approval_digest")),
        "records_digest_bound": (EXPECTED_RECORDS_DIGEST, candidate.get("records_digest")),
        "identity_freeze_digest_bound": (EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST, candidate.get("identity_authority_freeze_digest")),
        "target_universe_count_12": (12, candidate.get("target_universe_count")),
        "target_universe_matches_frozen_canonical_dataset_universe": (TARGET_UNIVERSE, candidate.get("target_universe")),
        "canonical_dataset_generated_true": (True, candidate.get("canonical_dataset_generated")),
        "canonical_dataset_frozen_true": (True, candidate.get("canonical_dataset_frozen")),
        "ready_for_research_registry_candidate_true": (True, candidate.get("ready_for_research_registry_candidate")),
        "research_registry_candidate_created_true": (True, candidate.get("research_registry_candidate_created")),
        "research_registry_candidate_scope_candidate_only": (RESEARCH_REGISTRY_CANDIDATE_SCOPE, candidate.get("research_registry_candidate_scope")),
        "research_registry_authority_status_not_approved": (RESEARCH_REGISTRY_AUTHORITY_STATUS, candidate.get("research_registry_authority_status")),
        "total_canonical_record_count_11946": (11946, candidate.get("total_canonical_record_count")),
        "meta_record_count_913_preserved": (913, counts.get("META")),
        "non_meta_record_counts_1003_preserved": (True, bool(counts) and all(count == 1003 for ticker, count in counts.items() if ticker != "META")),
        "registry_metadata_defined": (REGISTRY_CANDIDATE_METADATA, candidate.get("registry_candidate_metadata")),
        "registry_planning_dimensions_defined": (REGISTRY_PLANNING_DIMENSIONS, candidate.get("registry_planning_dimensions")),
        "future_registry_chain_defined": (FUTURE_REGISTRY_CHAIN, candidate.get("future_registry_chain")),
        "future_gates_defined": (FUTURE_GATES, candidate.get("future_gates")),
        "risk_controls_defined": (RISK_CONTROLS, candidate.get("risk_controls")),
        "planned_outputs_not_generated": (True, bool(planned) and all(row.get("generation_status") == PLANNED_NOT_GENERATED for row in planned)),
        "planned_outputs_research_only": (True, bool(planned) and all(row.get("output_label") == RESEARCH_ONLY_NON_ACTIONABLE for row in planned)),
        "provider_requests_made_false": (False, candidate.get("provider_requests_made")),
        "live_provider_transport_enabled_false": (False, candidate.get("live_provider_transport_enabled")),
        "market_data_acquisition_performed_false": (False, candidate.get("market_data_acquisition_performed")),
        "dataset_generation_performed_false": (False, candidate.get("dataset_generation_performed")),
        "canonical_dataset_regenerated_false": (False, candidate.get("canonical_dataset_regenerated")),
        "registry_approval_created_false": (False, candidate.get("registry_approval_created")),
        "additional_predictive_evidence_execution_authorized_false": (False, candidate.get("additional_predictive_evidence_execution_authorized")),
        "additional_predictive_evidence_executed_false": (False, candidate.get("additional_predictive_evidence_executed")),
        "predictive_experiment_rerun_authorized_false": (False, candidate.get("predictive_experiment_rerun_authorized")),
        "new_strategy_scoring_performed_false": (False, candidate.get("new_strategy_scoring_performed")),
        "trade_recommendations_generated_false": (False, candidate.get("trade_recommendations_generated")),
        "predictive_usefulness_not_accepted": (NOT_ACCEPTED, candidate.get("predictive_usefulness")),
        "profitability_not_accepted": (NOT_ACCEPTED, candidate.get("profitability")),
        "runtime_migration_approved_false": (False, candidate.get("runtime_migration_approved")),
        "runtime_use_not_authorized": (NOT_AUTHORIZED, candidate.get("runtime_use")),
        "strategy_use_not_authorized": (NOT_AUTHORIZED, candidate.get("strategy_use")),
        "paper_trading_not_authorized": (NOT_AUTHORIZED, candidate.get("paper_trading")),
        "broker_execution_not_authorized": (NOT_AUTHORIZED, candidate.get("broker_execution")),
        "automatic_stitching_false": (False, candidate.get("automatic_stitching")),
        "no_registry_approval_artifact_created": (False, candidate.get("registry_approval_artifact_created")),
        "no_predictive_usefulness_acceptance_artifact_created": (False, candidate.get("predictive_usefulness_acceptance_artifact_created")),
        "no_profitability_acceptance_created": (False, candidate.get("profitability_acceptance_created")),
        "no_runtime_migration_approval_created": (False, candidate.get("runtime_migration_approval_created")),
    }
    return [_check(check_id, *values[check_id]) for check_id in REQUIRED_CHECK_IDS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [row for row in checklist if row.get("status") != PASS]
    return {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row.get("severity") == BLOCKER for row in failed),
        "ready_for_operator_review": not failed,
        "ready_for_research_registry_approval": False,
        "registry_approval_created": False,
        "research_registry_approved": False,
        "additional_predictive_evidence_execution_authorized": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def research_registry_candidate_digest_v1(candidate: dict[str, Any]) -> str:
    payload = deepcopy(candidate)
    payload.pop("research_registry_candidate_digest", None)
    return semantic_digest(payload)


def build_research_registry_candidate_v1(
    *, canonical_dataset_frozen_artifact: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a candidate only; never create registry approval or runtime authority."""
    source, binding_mode = _source_freeze(canonical_dataset_frozen_artifact)
    candidate = _base_candidate(source, binding_mode)
    candidate["candidate_checklist"] = _checklist(candidate)
    candidate["candidate_summary"] = _summary(candidate["candidate_checklist"])
    candidate["research_registry_candidate_digest"] = research_registry_candidate_digest_v1(candidate)
    validate_research_registry_candidate_v1(candidate)
    return candidate


def _validate_per_ticker(candidate: dict[str, Any]) -> None:
    entries = candidate.get("per_ticker_research_registry_candidates")
    if not isinstance(entries, list) or len(entries) != 12:
        raise ResearchRegistryCandidateError("per-ticker registry candidate entries mismatch")
    _expect([row.get("ticker") for row in entries], TARGET_UNIVERSE, "per-ticker order")
    for row in entries:
        ticker = row["ticker"]
        expected = {
            "identity_authority_status": "FROZEN",
            "corporate_action_authority_status": "APPROVED",
            "acquisition_generation_status": "FROZEN",
            "canonical_dataset_status": "FROZEN",
            "research_registry_candidate_status": PLANNED_READY_FOR_OPERATOR_REVIEW,
            "historical_record_count": EXPECTED_RECORD_COUNTS[ticker],
            "meta_reduced_record_count_flag": ticker == "META",
            "registry_approval_created": False,
            "predictive_usefulness": NOT_ACCEPTED,
            "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
        }
        for field, value in expected.items():
            _expect(row.get(field), value, f"{ticker}.{field}")
        digest = row.get("per_ticker_research_registry_candidate_digest")
        _expect_digest(digest, f"{ticker}.per_ticker_research_registry_candidate_digest")
        _expect(digest, per_ticker_research_registry_candidate_digest_v1(row), f"{ticker}.candidate digest")


def validate_research_registry_candidate_v1(candidate: dict[str, Any]) -> dict[str, Any]:
    """Validate source bindings, planning content, and every closed authority gate."""
    if not isinstance(candidate, dict):
        raise ResearchRegistryCandidateError("candidate must be an object")
    expected = {
        "artifact_kind": ARTIFACT_KIND_RESEARCH_REGISTRY_CANDIDATE,
        "schema_version": SCHEMA_VERSION_RESEARCH_REGISTRY_CANDIDATE_V1,
        "candidate_status": RESEARCH_REGISTRY_READY_FOR_OPERATOR_REVIEW,
        "canonical_dataset_freeze_digest": EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST,
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
        "canonical_dataset_freeze_scope": freeze.CANONICAL_DATASET_FREEZE_ONLY,
        "target_universe": TARGET_UNIVERSE,
        "target_universe_count": 12,
        "source_profile": SOURCE_PROFILE,
        "total_canonical_record_count": 11946,
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "per_ticker_record_counts": EXPECTED_RECORD_COUNTS,
        "research_registry_candidate_objective": RESEARCH_REGISTRY_CANDIDATE_OBJECTIVE,
        "research_registry_candidate_scope": RESEARCH_REGISTRY_CANDIDATE_SCOPE,
        "research_registry_mode": RESEARCH_REGISTRY_MODE,
        "research_registry_authority_status": RESEARCH_REGISTRY_AUTHORITY_STATUS,
        "source_freeze_blocker_count": 0,
        "corporate_action_authority_scope": "CORPORATE_ACTION_AUTHORITY_ONLY",
        "split_event_authority_scope": "SPLIT_EVENT_AUTHORITY_ONLY",
        "dividend_event_authority_scope": "DIVIDEND_EVENT_AUTHORITY_ONLY",
        "registry_candidate_metadata": REGISTRY_CANDIDATE_METADATA,
        "registry_planning_dimensions": REGISTRY_PLANNING_DIMENSIONS,
        "future_registry_chain": FUTURE_REGISTRY_CHAIN,
        "future_gates": FUTURE_GATES,
        "risk_controls": RISK_CONTROLS,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
    }
    for field, value in expected.items():
        _expect(candidate.get(field), value, field)
    for field in (
        "created_offline", "research_registry_candidate_created",
        "research_registry_candidate_ready_for_operator_review", "canonical_dataset_generated",
        "canonical_dataset_frozen", "ready_for_research_registry_candidate",
        "dataset_generation_authorized", "canonical_dataset_authorized",
        "canonical_dataset_generation_approved", "new_ticker_acquisition_authorized",
        "acquisition_generation_authorized", "acquisition_generation_approved",
        "acquisition_generation_frozen", "corporate_action_authority_created",
        "corporate_action_authority_approved", "split_event_authority_created",
        "split_event_authority_frozen", "dividend_event_authority_created",
        "dividend_event_authority_frozen", "identity_authority_created",
        "identity_authority_frozen", "research_only", "operator_review_required",
    ):
        _expect_true(candidate.get(field), field)
    for field in (
        "provider_requests_made", "live_provider_transport_enabled",
        "market_data_acquisition_performed", "dataset_generation_performed",
        "canonical_dataset_regenerated", "raw_provider_payloads_committed",
        "api_keys_stored_or_printed", "research_registry_approved", "registry_approval_created",
        "additional_predictive_evidence_execution_authorized", "additional_predictive_evidence_executed",
        "predictive_experiment_rerun_authorized", "predictive_experiment_rerun_performed",
        "feature_matrix_regeneration_performed", "new_strategy_scoring_performed",
        "trade_recommendations_generated", "runtime_migration_approved", "runtime_migration_active",
        "automatic_stitching", "registry_approval_artifact_created",
        "predictive_usefulness_acceptance_artifact_created", "profitability_acceptance_created",
        "runtime_migration_approval_created",
    ):
        _expect_false(candidate.get(field), field)
    planned = candidate.get("planned_outputs")
    if not isinstance(planned, list) or len(planned) != len(PLANNED_OUTPUT_NAMES):
        raise ResearchRegistryCandidateError("planned_outputs mismatch")
    _expect([row.get("planned_output") for row in planned], PLANNED_OUTPUT_NAMES, "planned output names")
    for row in planned:
        _expect(row.get("generation_status"), PLANNED_NOT_GENERATED, "planned output status")
        _expect(row.get("output_label"), RESEARCH_ONLY_NON_ACTIONABLE, "planned output label")
    _validate_per_ticker(candidate)
    checklist = candidate.get("candidate_checklist")
    if not isinstance(checklist, list):
        raise ResearchRegistryCandidateError("candidate_checklist missing")
    _expect([row.get("check_id") for row in checklist], REQUIRED_CHECK_IDS, "candidate checklist ids")
    _expect(checklist, _checklist(candidate), "candidate checklist")
    if any(row.get("status") != PASS or row.get("severity") != BLOCKER for row in checklist):
        raise ResearchRegistryCandidateError("candidate checklist must pass")
    _expect(candidate.get("candidate_summary"), _summary(checklist), "candidate_summary")
    digest = candidate.get("research_registry_candidate_digest")
    _expect_digest(digest, "research_registry_candidate_digest")
    _expect(digest, research_registry_candidate_digest_v1(candidate), "research_registry_candidate_digest")
    return {
        "status": RESEARCH_REGISTRY_READY_FOR_OPERATOR_REVIEW,
        "research_registry_candidate_digest": digest,
        "total_checks": candidate["candidate_summary"]["total_checks"],
        "passed_checks": candidate["candidate_summary"]["passed_checks"],
        "failed_checks": candidate["candidate_summary"]["failed_checks"],
        "blocker_count": candidate["candidate_summary"]["blocker_count"],
    }


def build_research_registry_candidate_markdown_v1(candidate: dict[str, Any]) -> str:
    """Render the candidate and its explicit non-approval boundaries."""
    validation = validate_research_registry_candidate_v1(candidate)
    sections = [
        ("Research Registry Candidate", [f"Artifact/status: `{candidate['artifact_kind']}` / `{validation['status']}`.", f"Candidate digest: `{validation['research_registry_candidate_digest']}`."]),
        ("Source Frozen Canonical Dataset", [f"Freeze/review/generation digests: `{candidate['canonical_dataset_freeze_digest']}` / `{candidate['canonical_dataset_results_review_package_digest']}` / `{candidate['canonical_dataset_generation_digest']}`."]),
        ("Target Universe", [", ".join(f"`{ticker}`" for ticker in candidate["target_universe"]) + "."]),
        ("Registry Candidate Metadata", [f"`{key}`: `{value}`." for key, value in candidate["registry_candidate_metadata"].items()]),
        ("Per-Ticker Registry Candidate Entries", [f"`{row['ticker']}`: `{row['research_registry_candidate_status']}`, `{row['historical_record_count']}` records." for row in candidate["per_ticker_research_registry_candidates"]]),
        ("Future Registry Chain", [f"`{item}`" for item in candidate["future_registry_chain"]]),
        ("Future Gates", [f"`{item}`" for item in candidate["future_gates"]]),
        ("Risk Controls", [f"`{item}`" for item in candidate["risk_controls"]]),
        ("Registry Approval Boundary", ["The candidate is ready for operator review but creates no registry approval."]),
        ("Predictive/Profitability Boundary", ["Predictive usefulness and profitability remain not accepted."]),
        ("Runtime Boundary", ["Runtime, strategy, paper trading, and broker execution remain `NOT_AUTHORIZED`."]),
        ("Checklist Summary", [f"Total/passed/failed/blockers: `{validation['total_checks']} / {validation['passed_checks']} / {validation['failed_checks']} / {validation['blocker_count']}`."]),
        ("Guardrails", ["No provider request, acquisition, dataset regeneration, registry approval, predictive acceptance, runtime activation, or trading action occurred."]),
    ]
    lines = ["# MarketFlow Research Registry Candidate v1", "", "## Title", "", "- Research Registry Candidate v1.", ""]
    for title, body in sections:
        lines.extend([f"## {title}", "", *[f"- {item}" for item in body], ""])
    return "\n".join(lines)


def write_research_registry_candidate_v1(
    output_dir: str | Path, *, canonical_dataset_frozen_artifact: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Write canonical candidate JSON without overwriting an existing artifact."""
    candidate = build_research_registry_candidate_v1(
        canonical_dataset_frozen_artifact=canonical_dataset_frozen_artifact
    )
    validation = validate_research_registry_candidate_v1(candidate)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "research_registry_candidate_v1.json"
    if path.exists():
        raise ResearchRegistryCandidateError("research registry candidate output already exists")
    payload = canonical_json_bytes(candidate)
    path.write_bytes(payload)
    return {
        "path": str(path),
        "artifact_kind": candidate["artifact_kind"],
        "candidate_status": candidate["candidate_status"],
        "research_registry_candidate_digest": validation["research_registry_candidate_digest"],
        "payload_sha256": sha256_bytes(payload),
    }
