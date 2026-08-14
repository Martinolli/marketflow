"""Offline operator review for a canonical-dataset-chain candidate."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import canonical_dataset_chain_candidate_service as candidate_service


ARTIFACT_KIND_CANONICAL_DATASET_CHAIN_CANDIDATE_REVIEW_PACKAGE = (
    "CANONICAL_DATASET_CHAIN_CANDIDATE_REVIEW_PACKAGE"
)
SCHEMA_VERSION_CANONICAL_DATASET_CHAIN_CANDIDATE_REVIEW_V1 = (
    "canonical_dataset_chain_candidate_review_v1"
)
CANONICAL_DATASET_CHAIN_CANDIDATE_REVIEW_PACKAGE_READY = (
    "CANONICAL_DATASET_CHAIN_CANDIDATE_REVIEW_PACKAGE_READY"
)
READY_FOR_OPERATOR_ASSESSMENT = "READY_FOR_OPERATOR_ASSESSMENT"
EXPECTED_REVIEWED_CANONICAL_DATASET_CHAIN_CANDIDATE_DIGEST = (
    "d57a39e246b8e31ca96bec4bdf027ed49ee9afc6ba07c9ac7c0e7c7eb3581053"
)
EXPECTED_REVIEWED_CANDIDATE_CHECKLIST_TOTAL = 51
EXPECTED_REVIEWED_CANDIDATE_CHECKLIST_PASSED = 51
EXPECTED_REVIEWED_CANDIDATE_CHECKLIST_FAILED = 0
EXPECTED_REVIEWED_CANDIDATE_BLOCKER_COUNT = 0

TARGET_UNIVERSE = list(candidate_service.TARGET_UNIVERSE)
PASS = candidate_service.PASS
FAIL = candidate_service.FAIL
BLOCKER = candidate_service.BLOCKER
NOT_AUTHORIZED = candidate_service.NOT_AUTHORIZED
NOT_ACCEPTED = candidate_service.NOT_ACCEPTED
PROFITABILITY_NOT_ACCEPTED = candidate_service.PROFITABILITY_NOT_ACCEPTED

REQUIRED_CHECK_IDS = [
    "candidate_kind_matches",
    "candidate_status_ready_for_review",
    "candidate_digest_matches_expected",
    "candidate_checklist_zero_blockers",
    "acquisition_generation_freeze_digest_bound",
    "acquisition_generation_approval_digest_bound",
    "acquisition_evidence_results_review_digest_bound",
    "corporate_action_authority_approval_digest_bound",
    "identity_freeze_digest_bound",
    "target_universe_count_12",
    "target_universe_matches_candidate_universe",
    "acquisition_generation_frozen_true",
    "ready_for_canonical_dataset_chain_candidate_true",
    "canonical_dataset_chain_candidate_created_true",
    "canonical_dataset_chain_review_created_true",
    "canonical_dataset_chain_scope_candidate_only",
    "canonical_dataset_authority_status_not_authorized",
    "per_ticker_canonical_dataset_chain_entries_12",
    "per_ticker_canonical_dataset_chain_review_entries_12",
    "per_ticker_canonical_dataset_chain_candidate_digests_present",
    "per_ticker_canonical_dataset_chain_review_digests_present",
    "canonical_dataset_planning_dimensions_reviewed",
    "source_profile_preserved",
    "meta_reduced_bar_count_preserved",
    "future_canonical_dataset_chain_reviewed",
    "future_gates_defined",
    "risk_controls_defined",
    "planned_outputs_10",
    "planned_outputs_not_generated",
    "planned_outputs_research_only",
    "provider_requests_made_in_review_false",
    "live_provider_transport_enabled_in_review_false",
    "market_data_acquisition_performed_in_review_false",
    "dataset_generation_performed_in_review_false",
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


class CanonicalDatasetChainCandidateReviewPackageError(ValueError):
    """Raised when a canonical-dataset-chain review package is invalid."""


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise CanonicalDatasetChainCandidateReviewPackageError(f"{field} mismatch")


def _expect_true(actual: Any, field: str) -> None:
    if actual is not True:
        raise CanonicalDatasetChainCandidateReviewPackageError(f"{field} must be true")


def _expect_false(actual: Any, field: str) -> None:
    if actual is not False:
        raise CanonicalDatasetChainCandidateReviewPackageError(f"{field} must be false")


def _expect_digest(actual: Any, field: str) -> None:
    if not isinstance(actual, str) or len(actual) != 64:
        raise CanonicalDatasetChainCandidateReviewPackageError(f"{field} missing")


def _candidate_for_binding(candidate: dict[str, Any] | None) -> dict[str, Any]:
    source = (
        candidate_service.build_canonical_dataset_chain_candidate_v1()
        if candidate is None
        else deepcopy(candidate)
    )
    try:
        validation = candidate_service.validate_canonical_dataset_chain_candidate_v1(source)
    except candidate_service.CanonicalDatasetChainCandidateError as exc:
        raise CanonicalDatasetChainCandidateReviewPackageError(
            f"reviewed candidate invalid: {exc}"
        ) from exc
    _expect(
        validation.get("canonical_dataset_chain_candidate_digest"),
        EXPECTED_REVIEWED_CANONICAL_DATASET_CHAIN_CANDIDATE_DIGEST,
        "reviewed candidate digest",
    )
    _expect(validation.get("blocker_count"), 0, "reviewed candidate blocker_count")
    return source


def per_ticker_canonical_dataset_chain_review_digest_v1(entry: dict[str, Any]) -> str:
    payload = deepcopy(entry)
    payload.pop("per_ticker_canonical_dataset_chain_review_digest", None)
    return semantic_digest(payload)


def _review_entries(source: dict[str, Any]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for row in source["per_ticker_canonical_dataset_chain_candidates"]:
        entry = deepcopy(row)
        entry["canonical_dataset_chain_review_status"] = READY_FOR_OPERATOR_ASSESSMENT
        entry["source_canonical_dataset_chain_candidate_digest"] = source[
            "canonical_dataset_chain_candidate_digest"
        ]
        entry["per_ticker_canonical_dataset_chain_review_digest"] = (
            per_ticker_canonical_dataset_chain_review_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _base_review_package(source: dict[str, Any]) -> dict[str, Any]:
    copied_fields = [
        "acquisition_generation_freeze_digest",
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
        "post_identity_freeze_registry_inventory_approval_digest",
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
        "ready_for_canonical_dataset_chain_candidate",
        "canonical_dataset_chain_objective",
        "canonical_dataset_chain_scope",
        "canonical_dataset_mode",
        "canonical_dataset_authority_status",
        "meta_reduced_bar_count_preserved",
    ]
    review = {field: deepcopy(source[field]) for field in copied_fields}
    review.update({
        "artifact_kind": ARTIFACT_KIND_CANONICAL_DATASET_CHAIN_CANDIDATE_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_CANONICAL_DATASET_CHAIN_CANDIDATE_REVIEW_V1,
        "review_status": CANONICAL_DATASET_CHAIN_CANDIDATE_REVIEW_PACKAGE_READY,
        "created_offline": True,
        "provider_requests_made_in_review": False,
        "live_provider_transport_enabled_in_review": False,
        "market_data_acquisition_performed_in_review": False,
        "dataset_generation_performed_in_review": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "canonical_dataset_chain_candidate_created": True,
        "canonical_dataset_chain_candidate_review_created": True,
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
        "reviewed_canonical_dataset_chain_candidate_kind": source["artifact_kind"],
        "reviewed_canonical_dataset_chain_candidate_status": source["candidate_status"],
        "reviewed_canonical_dataset_chain_candidate_digest": source["canonical_dataset_chain_candidate_digest"],
        "reviewed_canonical_dataset_chain_candidate_checklist_total": source["candidate_summary"]["total_checks"],
        "reviewed_canonical_dataset_chain_candidate_checklist_passed": source["candidate_summary"]["passed_checks"],
        "reviewed_canonical_dataset_chain_candidate_checklist_failed": source["candidate_summary"]["failed_checks"],
        "reviewed_canonical_dataset_chain_candidate_blocker_count": source["candidate_summary"]["blocker_count"],
        "reviewed_canonical_dataset_planning_dimensions": deepcopy(source["canonical_dataset_planning_dimensions"]),
        "reviewed_canonical_dataset_source_profile": deepcopy(source["canonical_dataset_source_profile"]),
        "reviewed_per_ticker_canonical_dataset_chain_entries": _review_entries(source),
        "reviewed_future_canonical_dataset_chain": deepcopy(source["future_canonical_dataset_chain"]),
        "reviewed_future_gates": deepcopy(source["future_gates"]),
        "reviewed_risk_controls": deepcopy(source["risk_controls"]),
        "reviewed_planned_outputs": deepcopy(source["planned_outputs"]),
        "planned_output_count": len(source["planned_outputs"]),
        "planned_outputs_status": candidate_service.PLANNED_NOT_GENERATED,
        "planned_outputs_label": candidate_service.RESEARCH_ONLY_NON_ACTIONABLE,
        "dataset_generation_artifact_created": False,
        "canonical_dataset_artifact_created": False,
        "registry_approval_artifact_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
    })
    return review


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


def _checklist(review: dict[str, Any]) -> list[dict[str, Any]]:
    entries = review["reviewed_per_ticker_canonical_dataset_chain_entries"]
    outputs = review["reviewed_planned_outputs"]
    values: dict[str, tuple[Any, Any]] = {
        "candidate_kind_matches": (candidate_service.ARTIFACT_KIND_CANONICAL_DATASET_CHAIN_CANDIDATE, review.get("reviewed_canonical_dataset_chain_candidate_kind")),
        "candidate_status_ready_for_review": (candidate_service.CANONICAL_DATASET_CHAIN_READY_FOR_OPERATOR_REVIEW, review.get("reviewed_canonical_dataset_chain_candidate_status")),
        "candidate_digest_matches_expected": (EXPECTED_REVIEWED_CANONICAL_DATASET_CHAIN_CANDIDATE_DIGEST, review.get("reviewed_canonical_dataset_chain_candidate_digest")),
        "candidate_checklist_zero_blockers": (0, review.get("reviewed_canonical_dataset_chain_candidate_blocker_count")),
        "acquisition_generation_freeze_digest_bound": (candidate_service.EXPECTED_ACQUISITION_GENERATION_FREEZE_DIGEST, review.get("acquisition_generation_freeze_digest")),
        "acquisition_generation_approval_digest_bound": (candidate_service.EXPECTED_ACQUISITION_GENERATION_APPROVAL_DIGEST, review.get("acquisition_generation_approval_digest")),
        "acquisition_evidence_results_review_digest_bound": (candidate_service.EXPECTED_ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST, review.get("acquisition_evidence_results_review_package_digest")),
        "corporate_action_authority_approval_digest_bound": (candidate_service.EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST, review.get("corporate_action_authority_approval_digest")),
        "identity_freeze_digest_bound": (candidate_service.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST, review.get("identity_authority_freeze_digest")),
        "target_universe_count_12": (12, review.get("target_universe_count")),
        "target_universe_matches_candidate_universe": (TARGET_UNIVERSE, review.get("target_universe")),
        "acquisition_generation_frozen_true": (True, review.get("acquisition_generation_frozen")),
        "ready_for_canonical_dataset_chain_candidate_true": (True, review.get("ready_for_canonical_dataset_chain_candidate")),
        "canonical_dataset_chain_candidate_created_true": (True, review.get("canonical_dataset_chain_candidate_created")),
        "canonical_dataset_chain_review_created_true": (True, review.get("canonical_dataset_chain_candidate_review_created")),
        "canonical_dataset_chain_scope_candidate_only": (candidate_service.CANONICAL_DATASET_CHAIN_SCOPE, review.get("canonical_dataset_chain_scope")),
        "canonical_dataset_authority_status_not_authorized": (candidate_service.CANONICAL_DATASET_AUTHORITY_STATUS, review.get("canonical_dataset_authority_status")),
        "per_ticker_canonical_dataset_chain_entries_12": (12, len(entries)),
        "per_ticker_canonical_dataset_chain_review_entries_12": (12, len(entries)),
        "per_ticker_canonical_dataset_chain_candidate_digests_present": (True, bool(entries) and all(isinstance(row.get("per_ticker_canonical_dataset_chain_candidate_digest"), str) and len(row["per_ticker_canonical_dataset_chain_candidate_digest"]) == 64 for row in entries)),
        "per_ticker_canonical_dataset_chain_review_digests_present": (True, bool(entries) and all(isinstance(row.get("per_ticker_canonical_dataset_chain_review_digest"), str) and len(row["per_ticker_canonical_dataset_chain_review_digest"]) == 64 for row in entries)),
        "canonical_dataset_planning_dimensions_reviewed": (candidate_service.CANONICAL_DATASET_PLANNING_DIMENSIONS, review.get("reviewed_canonical_dataset_planning_dimensions")),
        "source_profile_preserved": (candidate_service.SOURCE_PROFILE, review.get("reviewed_canonical_dataset_source_profile")),
        "meta_reduced_bar_count_preserved": (True, review.get("meta_reduced_bar_count_preserved")),
        "future_canonical_dataset_chain_reviewed": (candidate_service.FUTURE_CANONICAL_DATASET_CHAIN, review.get("reviewed_future_canonical_dataset_chain")),
        "future_gates_defined": (candidate_service.FUTURE_GATES, review.get("reviewed_future_gates")),
        "risk_controls_defined": (candidate_service.RISK_CONTROLS, review.get("reviewed_risk_controls")),
        "planned_outputs_10": (10, review.get("planned_output_count")),
        "planned_outputs_not_generated": (True, bool(outputs) and all(row.get("generation_status") == candidate_service.PLANNED_NOT_GENERATED for row in outputs)),
        "planned_outputs_research_only": (True, bool(outputs) and all(row.get("classification") == candidate_service.RESEARCH_ONLY_NON_ACTIONABLE for row in outputs)),
        "predictive_usefulness_not_accepted": (NOT_ACCEPTED, review.get("predictive_usefulness")),
        "profitability_not_accepted": (PROFITABILITY_NOT_ACCEPTED, review.get("profitability")),
        "runtime_use_not_authorized": (NOT_AUTHORIZED, review.get("runtime_use")),
        "strategy_use_not_authorized": (NOT_AUTHORIZED, review.get("strategy_use")),
        "paper_trading_not_authorized": (NOT_AUTHORIZED, review.get("paper_trading")),
        "broker_execution_not_authorized": (NOT_AUTHORIZED, review.get("broker_execution")),
    }
    false_checks = {
        "provider_requests_made_in_review_false": "provider_requests_made_in_review",
        "live_provider_transport_enabled_in_review_false": "live_provider_transport_enabled_in_review",
        "market_data_acquisition_performed_in_review_false": "market_data_acquisition_performed_in_review",
        "dataset_generation_performed_in_review_false": "dataset_generation_performed_in_review",
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
    values.update({check_id: (False, review.get(field)) for check_id, field in false_checks.items()})
    return [_check(check_id, *values[check_id]) for check_id in REQUIRED_CHECK_IDS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [row for row in checklist if row["status"] != PASS]
    return {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row["severity"] == BLOCKER for row in failed),
        "ready_for_operator_assessment": not failed,
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


def canonical_dataset_chain_candidate_review_package_digest_v1(review_package: dict[str, Any]) -> str:
    payload = deepcopy(review_package)
    payload.pop("canonical_dataset_chain_candidate_review_package_digest", None)
    return semantic_digest(payload)


def build_canonical_dataset_chain_candidate_review_package_v1(
    candidate: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a deterministic review package without provider or dataset work."""
    review = _base_review_package(_candidate_for_binding(candidate))
    review["review_checklist"] = _checklist(review)
    review["review_summary"] = _summary(review["review_checklist"])
    review["canonical_dataset_chain_candidate_review_package_digest"] = (
        canonical_dataset_chain_candidate_review_package_digest_v1(review)
    )
    validate_canonical_dataset_chain_candidate_review_package_v1(review)
    return review


def _validate_per_ticker(review: dict[str, Any]) -> None:
    entries = review.get("reviewed_per_ticker_canonical_dataset_chain_entries")
    if not isinstance(entries, list) or len(entries) != 12:
        raise CanonicalDatasetChainCandidateReviewPackageError("per_ticker review entries mismatch")
    _expect([row.get("ticker") for row in entries], TARGET_UNIVERSE, "per_ticker tickers")
    for row in entries:
        ticker = row["ticker"]
        expected = {
            "identity_authority_status": "FROZEN",
            "split_event_authority_status": "FROZEN",
            "dividend_event_authority_status": "FROZEN",
            "corporate_action_authority_status": "APPROVED",
            "acquisition_generation_status": "FROZEN",
            "canonical_dataset_chain_status": candidate_service.PLANNED_READY_FOR_OPERATOR_REVIEW,
            "canonical_dataset_chain_review_status": READY_FOR_OPERATOR_ASSESSMENT,
            "historical_bar_evidence_status": candidate_service.ACQUISITION_EVIDENCE_COLLECTED_READ_ONLY,
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
            "source_canonical_dataset_chain_candidate_digest": EXPECTED_REVIEWED_CANONICAL_DATASET_CHAIN_CANDIDATE_DIGEST,
        }
        for field, value in expected.items():
            _expect(row.get(field), value, f"{ticker}.{field}")
        candidate_digest = row.get("per_ticker_canonical_dataset_chain_candidate_digest")
        _expect_digest(candidate_digest, f"{ticker}.candidate digest")
        review_digest = row.get("per_ticker_canonical_dataset_chain_review_digest")
        _expect_digest(review_digest, f"{ticker}.review digest")
        _expect(review_digest, per_ticker_canonical_dataset_chain_review_digest_v1(row), f"{ticker}.review digest")


def validate_canonical_dataset_chain_candidate_review_package_v1(
    review_package: dict[str, Any],
) -> dict[str, Any]:
    """Validate exact reviewed evidence and all closed authority gates."""
    if not isinstance(review_package, dict):
        raise CanonicalDatasetChainCandidateReviewPackageError("review_package must be an object")
    expected = {
        "artifact_kind": ARTIFACT_KIND_CANONICAL_DATASET_CHAIN_CANDIDATE_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_CANONICAL_DATASET_CHAIN_CANDIDATE_REVIEW_V1,
        "review_status": CANONICAL_DATASET_CHAIN_CANDIDATE_REVIEW_PACKAGE_READY,
        "reviewed_canonical_dataset_chain_candidate_kind": candidate_service.ARTIFACT_KIND_CANONICAL_DATASET_CHAIN_CANDIDATE,
        "reviewed_canonical_dataset_chain_candidate_status": candidate_service.CANONICAL_DATASET_CHAIN_READY_FOR_OPERATOR_REVIEW,
        "reviewed_canonical_dataset_chain_candidate_digest": EXPECTED_REVIEWED_CANONICAL_DATASET_CHAIN_CANDIDATE_DIGEST,
        "reviewed_canonical_dataset_chain_candidate_checklist_total": EXPECTED_REVIEWED_CANDIDATE_CHECKLIST_TOTAL,
        "reviewed_canonical_dataset_chain_candidate_checklist_passed": EXPECTED_REVIEWED_CANDIDATE_CHECKLIST_PASSED,
        "reviewed_canonical_dataset_chain_candidate_checklist_failed": EXPECTED_REVIEWED_CANDIDATE_CHECKLIST_FAILED,
        "reviewed_canonical_dataset_chain_candidate_blocker_count": EXPECTED_REVIEWED_CANDIDATE_BLOCKER_COUNT,
        "acquisition_generation_freeze_digest": candidate_service.EXPECTED_ACQUISITION_GENERATION_FREEZE_DIGEST,
        "acquisition_generation_approval_digest": candidate_service.EXPECTED_ACQUISITION_GENERATION_APPROVAL_DIGEST,
        "acquisition_evidence_results_review_package_digest": candidate_service.EXPECTED_ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        "corporate_action_authority_approval_digest": candidate_service.EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST,
        "identity_authority_freeze_digest": candidate_service.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
        "target_universe": TARGET_UNIVERSE,
        "target_universe_count": 12,
        "canonical_dataset_chain_objective": candidate_service.CANONICAL_DATASET_CHAIN_OBJECTIVE,
        "canonical_dataset_chain_scope": candidate_service.CANONICAL_DATASET_CHAIN_SCOPE,
        "canonical_dataset_mode": candidate_service.CANONICAL_DATASET_MODE,
        "canonical_dataset_authority_status": candidate_service.CANONICAL_DATASET_AUTHORITY_STATUS,
        "reviewed_canonical_dataset_planning_dimensions": candidate_service.CANONICAL_DATASET_PLANNING_DIMENSIONS,
        "reviewed_canonical_dataset_source_profile": candidate_service.SOURCE_PROFILE,
        "reviewed_future_canonical_dataset_chain": candidate_service.FUTURE_CANONICAL_DATASET_CHAIN,
        "reviewed_future_gates": candidate_service.FUTURE_GATES,
        "reviewed_risk_controls": candidate_service.RISK_CONTROLS,
        "reviewed_planned_outputs": candidate_service._planned_outputs(),
        "planned_output_count": 10,
        "planned_outputs_status": candidate_service.PLANNED_NOT_GENERATED,
        "planned_outputs_label": candidate_service.RESEARCH_ONLY_NON_ACTIONABLE,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": PROFITABILITY_NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
    }
    for field, value in expected.items():
        _expect(review_package.get(field), value, field)
    for field in (
        "created_offline", "canonical_dataset_chain_candidate_created",
        "canonical_dataset_chain_candidate_review_created", "canonical_dataset_chain_ready_for_operator_review",
        "new_ticker_acquisition_authorized", "acquisition_generation_authorized",
        "acquisition_generation_approved", "acquisition_generation_frozen",
        "ready_for_canonical_dataset_chain_candidate", "corporate_action_authority_created",
        "corporate_action_authority_approved", "split_event_authority_created", "split_event_authority_frozen",
        "dividend_event_authority_created", "dividend_event_authority_frozen", "identity_authority_created",
        "identity_authority_frozen", "research_only", "operator_review_required", "meta_reduced_bar_count_preserved",
    ):
        _expect_true(review_package.get(field), field)
    for field in (
        "provider_requests_made_in_review", "live_provider_transport_enabled_in_review",
        "market_data_acquisition_performed_in_review", "dataset_generation_performed_in_review",
        "raw_provider_payloads_committed", "api_keys_stored_or_printed", "canonical_dataset_chain_approved",
        "dataset_generation_authorized", "canonical_dataset_authorized", "canonical_dataset_candidate_created",
        "canonical_dataset_generation_executed", "canonical_dataset_frozen", "registry_approval_created",
        "acquisition_generation_executed", "acquisition_generation_results_created",
        "additional_predictive_evidence_execution_authorized", "additional_predictive_evidence_executed",
        "predictive_experiment_rerun_authorized", "predictive_experiment_rerun_performed",
        "feature_matrix_regeneration_performed", "new_strategy_scoring_performed", "trade_recommendations_generated",
        "runtime_migration_approved", "runtime_migration_active", "automatic_stitching",
        "dataset_generation_artifact_created", "canonical_dataset_artifact_created",
        "registry_approval_artifact_created", "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_created", "runtime_migration_approval_created",
    ):
        _expect_false(review_package.get(field), field)
    _validate_per_ticker(review_package)
    checklist = review_package.get("review_checklist")
    if not isinstance(checklist, list):
        raise CanonicalDatasetChainCandidateReviewPackageError("review_checklist missing")
    _expect([row.get("check_id") for row in checklist], REQUIRED_CHECK_IDS, "review checklist ids")
    for row in checklist:
        _expect(row.get("status"), PASS, f"{row.get('check_id')}.status")
        _expect(row.get("severity"), BLOCKER, f"{row.get('check_id')}.severity")
    _expect(checklist, _checklist(review_package), "review checklist")
    _expect(review_package.get("review_summary"), _summary(checklist), "review summary")
    digest = review_package.get("canonical_dataset_chain_candidate_review_package_digest")
    _expect_digest(digest, "canonical_dataset_chain_candidate_review_package_digest")
    _expect(digest, canonical_dataset_chain_candidate_review_package_digest_v1(review_package), "review package digest")
    return {
        "status": CANONICAL_DATASET_CHAIN_CANDIDATE_REVIEW_PACKAGE_READY,
        "canonical_dataset_chain_candidate_review_package_digest": digest,
        "total_checks": review_package["review_summary"]["total_checks"],
        "passed_checks": review_package["review_summary"]["passed_checks"],
        "failed_checks": review_package["review_summary"]["failed_checks"],
        "blocker_count": review_package["review_summary"]["blocker_count"],
    }


def build_canonical_dataset_chain_candidate_review_markdown_v1(review_package: dict[str, Any]) -> str:
    validation = validate_canonical_dataset_chain_candidate_review_package_v1(review_package)
    summary = review_package["review_summary"]
    lines = [
        "# MarketFlow Canonical Dataset Chain Candidate Review Package v1", "",
        "## Canonical Dataset Chain Candidate Review Package",
        f"- Artifact/status: `{review_package['artifact_kind']}` / `{review_package['review_status']}`.",
        f"- Review digest: `{validation['canonical_dataset_chain_candidate_review_package_digest']}`.", "",
        "## Reviewed Candidate", f"- Candidate digest: `{review_package['reviewed_canonical_dataset_chain_candidate_digest']}`; checks/blockers: `51 / 0`.", "",
        "## Source Acquisition Generation Freeze", f"- Freeze digest: `{review_package['acquisition_generation_freeze_digest']}`.", "",
        "## Target Universe", "- " + ", ".join(f"`{ticker}`" for ticker in review_package["target_universe"]) + ".", "",
        "## Per-Ticker Canonical Dataset Chain Review Entries",
    ]
    lines.extend(f"- `{row['ticker']}`: `{row['canonical_dataset_chain_review_status']}`, bars `{row['historical_bar_count']}`." for row in review_package["reviewed_per_ticker_canonical_dataset_chain_entries"])
    lines.extend([
        "", "## Canonical Dataset Planning Dimensions", *[f"- `{item}`" for item in review_package["reviewed_canonical_dataset_planning_dimensions"]], "",
        "## Source Profile", *[f"- `{key}`: `{value}`." for key, value in review_package["reviewed_canonical_dataset_source_profile"].items()], "",
        "## Future Canonical Dataset Chain", *[f"- {item}" for item in review_package["reviewed_future_canonical_dataset_chain"]], "",
        "## Future Gates", *[f"- `{item}`" for item in review_package["reviewed_future_gates"]], "",
        "## Risk Controls", *[f"- `{item}`" for item in review_package["reviewed_risk_controls"]], "",
        "## Dataset Boundary", "- Dataset generation is neither authorized nor performed.", "",
        "## Canonical Dataset Boundary", "- No canonical dataset candidate, authorization, generation, or freeze was created.", "",
        "## Registry Boundary", "- No registry approval was created.", "",
        "## Predictive/Profitability Boundary", "- Predictive usefulness and profitability remain not accepted.", "",
        "## Runtime Boundary", "- Runtime, strategy, paper trading, and broker execution remain `NOT_AUTHORIZED`.", "",
        "## Checklist Summary", f"- Total/passed/failed/blockers: `{summary['total_checks']} / {summary['passed_checks']} / {summary['failed_checks']} / {summary['blocker_count']}`.", "",
        "## Guardrails", "- Review records evidence only; it grants no dataset, registry, predictive, runtime, or trading authority.",
    ])
    return "\n".join(lines) + "\n"


def write_canonical_dataset_chain_candidate_review_package_v1(
    output_dir: str | Path,
    *,
    candidate: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Write canonical review JSON without overwriting an existing artifact."""
    review = build_canonical_dataset_chain_candidate_review_package_v1(candidate)
    validation = validate_canonical_dataset_chain_candidate_review_package_v1(review)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "canonical_dataset_chain_candidate_review_package_v1.json"
    if path.exists():
        raise CanonicalDatasetChainCandidateReviewPackageError("canonical dataset chain review output already exists")
    payload = canonical_json_bytes(review)
    path.write_bytes(payload)
    return {
        "path": str(path), "artifact_kind": review["artifact_kind"],
        "review_status": review["review_status"],
        "canonical_dataset_chain_candidate_review_package_digest": validation["canonical_dataset_chain_candidate_review_package_digest"],
        "payload_sha256": sha256_bytes(payload),
    }
