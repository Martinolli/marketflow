"""Offline operator review for an acquisition-generation chain candidate."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest
from marketflow.services import acquisition_generation_chain_candidate_service as candidate_service


ARTIFACT_KIND_ACQUISITION_GENERATION_CHAIN_CANDIDATE_REVIEW_PACKAGE = (
    "ACQUISITION_GENERATION_CHAIN_CANDIDATE_REVIEW_PACKAGE"
)
SCHEMA_VERSION_ACQUISITION_GENERATION_CHAIN_CANDIDATE_REVIEW_V1 = (
    "acquisition_generation_chain_candidate_review_v1"
)
ACQUISITION_GENERATION_CHAIN_CANDIDATE_REVIEW_PACKAGE_READY = (
    "ACQUISITION_GENERATION_CHAIN_CANDIDATE_REVIEW_PACKAGE_READY"
)
ACQUISITION_GENERATION_CHAIN_CANDIDATE_STATUS_BINDING = (
    "ACQUISITION_GENERATION_CHAIN_CANDIDATE_STATUS_BINDING"
)
ACQUISITION_GENERATION_CHAIN_CANDIDATE_OBJECT_BINDING = (
    "ACQUISITION_GENERATION_CHAIN_CANDIDATE_OBJECT_BINDING"
)
READY_FOR_OPERATOR_ASSESSMENT = "READY_FOR_OPERATOR_ASSESSMENT"

EXPECTED_REVIEWED_ACQUISITION_GENERATION_CHAIN_CANDIDATE_DIGEST = (
    "e0fb0b3f2ccd4bdac3d8f24a6888e8a97d5013bcc33f1dee1d49ccd59204b4ff"
)
EXPECTED_REVIEWED_CANDIDATE_CHECKLIST_TOTAL = 57
EXPECTED_REVIEWED_CANDIDATE_CHECKLIST_PASSED = 57
EXPECTED_REVIEWED_CANDIDATE_CHECKLIST_FAILED = 0
EXPECTED_REVIEWED_CANDIDATE_BLOCKER_COUNT = 0

TARGET_UNIVERSE = list(candidate_service.TARGET_UNIVERSE)
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

REQUIRED_CHECK_IDS = [
    "candidate_kind_matches",
    "candidate_status_ready_for_review",
    "candidate_digest_matches_expected",
    "candidate_checklist_zero_blockers",
    "corporate_action_authority_approval_digest_bound",
    "combined_readiness_review_digest_bound",
    "split_authority_freeze_digest_bound",
    "dividend_authority_freeze_digest_bound",
    "identity_freeze_digest_bound",
    "target_universe_count_12",
    "target_universe_matches_candidate_universe",
    "corporate_action_authority_created_true",
    "corporate_action_authority_approved_true",
    "corporate_action_authority_scope_corporate_action_only",
    "split_event_authority_created_true",
    "split_event_authority_frozen_true",
    "dividend_event_authority_created_true",
    "dividend_event_authority_frozen_true",
    "ready_for_acquisition_generation_chain_candidate_true",
    "acquisition_generation_chain_candidate_created_true",
    "acquisition_generation_chain_review_created_true",
    "acquisition_chain_scope_candidate_only",
    "acquisition_generation_authority_status_not_authorized",
    "per_ticker_acquisition_chain_entries_12",
    "per_ticker_acquisition_chain_review_entries_12",
    "per_ticker_acquisition_chain_candidate_digests_present",
    "per_ticker_acquisition_chain_review_digests_present",
    "acquisition_planning_dimensions_reviewed",
    "future_acquisition_chain_reviewed",
    "future_provider_request_policy_reviewed",
    "future_gates_defined",
    "risk_controls_defined",
    "planned_outputs_9",
    "planned_outputs_not_generated",
    "planned_outputs_research_only",
    "provider_requests_made_in_review_false",
    "live_provider_transport_enabled_in_review_false",
    "market_data_acquisition_performed_in_review_false",
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
    "no_acquisition_authorization_artifact_created",
    "no_acquisition_execution_artifact_created",
    "no_dataset_generation_authorization_created",
    "no_canonical_dataset_artifact_created",
    "no_registry_approval_created",
    "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created",
    "no_runtime_migration_approval_created",
]


class AcquisitionGenerationChainCandidateReviewPackageError(ValueError):
    """Raised when the acquisition-chain candidate review package is invalid."""


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
        raise AcquisitionGenerationChainCandidateReviewPackageError(
            f"{field} mismatch"
        )


def _expect_true(actual: Any, field: str) -> None:
    if actual is not True:
        raise AcquisitionGenerationChainCandidateReviewPackageError(
            f"{field} must be true"
        )


def _expect_false(actual: Any, field: str) -> None:
    if actual is not False:
        raise AcquisitionGenerationChainCandidateReviewPackageError(
            f"{field} must be false"
        )


def _expect_digest(actual: Any, field: str) -> None:
    if not isinstance(actual, str) or len(actual) != 64:
        raise AcquisitionGenerationChainCandidateReviewPackageError(
            f"{field} missing"
        )


def _candidate_for_binding(
    candidate: dict[str, Any] | None,
) -> tuple[dict[str, Any], str]:
    if candidate is None:
        source = candidate_service.build_acquisition_generation_chain_candidate_v1()
        binding = ACQUISITION_GENERATION_CHAIN_CANDIDATE_STATUS_BINDING
    else:
        source = deepcopy(candidate)
        binding = ACQUISITION_GENERATION_CHAIN_CANDIDATE_OBJECT_BINDING
    validation = candidate_service.validate_acquisition_generation_chain_candidate_v1(
        source
    )
    _expect(
        validation.get("acquisition_generation_chain_candidate_digest"),
        EXPECTED_REVIEWED_ACQUISITION_GENERATION_CHAIN_CANDIDATE_DIGEST,
        "reviewed candidate digest",
    )
    _expect(validation.get("blocker_count"), 0, "reviewed candidate blocker_count")
    return source, binding


def per_ticker_acquisition_generation_chain_review_digest_v1(
    entry: dict[str, Any],
) -> str:
    payload = deepcopy(entry)
    payload.pop("per_ticker_acquisition_generation_chain_review_digest", None)
    return semantic_digest(payload)


def _review_entries(source: dict[str, Any]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    source_digest = source["acquisition_generation_chain_candidate_digest"]
    for source_entry in source[
        "per_ticker_acquisition_generation_chain_candidates"
    ]:
        entry = deepcopy(source_entry)
        entry["acquisition_generation_chain_review_status"] = (
            READY_FOR_OPERATOR_ASSESSMENT
        )
        entry["source_acquisition_generation_chain_candidate_digest"] = source_digest
        entry["per_ticker_acquisition_generation_chain_review_digest"] = (
            per_ticker_acquisition_generation_chain_review_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _base_review_package(
    source: dict[str, Any], binding_mode: str
) -> dict[str, Any]:
    review = deepcopy(source)
    review.pop("candidate_checklist")
    review.pop("candidate_summary")
    review.pop("acquisition_generation_chain_candidate_digest")
    review.pop("per_ticker_acquisition_generation_chain_candidates")
    review.update(
        {
            "artifact_kind": ARTIFACT_KIND_ACQUISITION_GENERATION_CHAIN_CANDIDATE_REVIEW_PACKAGE,
            "schema_version": SCHEMA_VERSION_ACQUISITION_GENERATION_CHAIN_CANDIDATE_REVIEW_V1,
            "review_status": ACQUISITION_GENERATION_CHAIN_CANDIDATE_REVIEW_PACKAGE_READY,
            "acquisition_generation_chain_candidate_binding_mode": binding_mode,
            "created_offline": True,
            "provider_requests_made_in_review": False,
            "live_provider_transport_enabled_in_review": False,
            "market_data_acquisition_performed_in_review": False,
            "acquisition_generation_chain_candidate_review_created": True,
            "reviewed_acquisition_generation_chain_candidate_kind": source[
                "artifact_kind"
            ],
            "reviewed_acquisition_generation_chain_candidate_status": source[
                "candidate_status"
            ],
            "reviewed_acquisition_generation_chain_candidate_digest": source[
                "acquisition_generation_chain_candidate_digest"
            ],
            "reviewed_acquisition_generation_chain_candidate_checklist_total": source[
                "candidate_summary"
            ]["total_checks"],
            "reviewed_acquisition_generation_chain_candidate_checklist_passed": source[
                "candidate_summary"
            ]["passed_checks"],
            "reviewed_acquisition_generation_chain_candidate_checklist_failed": source[
                "candidate_summary"
            ]["failed_checks"],
            "reviewed_acquisition_generation_chain_candidate_blocker_count": source[
                "candidate_summary"
            ]["blocker_count"],
            "reviewed_per_ticker_acquisition_generation_chain_candidate_entry_count": len(
                source["per_ticker_acquisition_generation_chain_candidates"]
            ),
            "per_ticker_acquisition_generation_chain_review_entries": _review_entries(
                source
            ),
            "planned_output_count": len(source["planned_outputs"]),
        }
    )
    return review


def _review_checklist(review: dict[str, Any]) -> list[dict[str, Any]]:
    entries = review.get("per_ticker_acquisition_generation_chain_review_entries", [])
    outputs = review.get("planned_outputs", [])
    values: dict[str, tuple[Any, Any]] = {
        "candidate_kind_matches": (candidate_service.ARTIFACT_KIND_ACQUISITION_GENERATION_CHAIN_CANDIDATE, review.get("reviewed_acquisition_generation_chain_candidate_kind")),
        "candidate_status_ready_for_review": (candidate_service.ACQUISITION_GENERATION_CHAIN_READY_FOR_OPERATOR_REVIEW, review.get("reviewed_acquisition_generation_chain_candidate_status")),
        "candidate_digest_matches_expected": (EXPECTED_REVIEWED_ACQUISITION_GENERATION_CHAIN_CANDIDATE_DIGEST, review.get("reviewed_acquisition_generation_chain_candidate_digest")),
        "candidate_checklist_zero_blockers": (0, review.get("reviewed_acquisition_generation_chain_candidate_blocker_count")),
        "corporate_action_authority_approval_digest_bound": (candidate_service.EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST, review.get("corporate_action_authority_approval_digest")),
        "combined_readiness_review_digest_bound": (candidate_service.EXPECTED_COMBINED_READINESS_REVIEW_PACKAGE_DIGEST, review.get("combined_split_dividend_corporate_action_readiness_review_package_digest")),
        "split_authority_freeze_digest_bound": (candidate_service.EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST, review.get("split_event_authority_freeze_digest")),
        "dividend_authority_freeze_digest_bound": (candidate_service.EXPECTED_DIVIDEND_EVENT_AUTHORITY_FREEZE_DIGEST, review.get("dividend_event_authority_freeze_digest")),
        "identity_freeze_digest_bound": (candidate_service.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST, review.get("identity_authority_freeze_digest")),
        "target_universe_count_12": (12, review.get("target_universe_count")),
        "target_universe_matches_candidate_universe": (TARGET_UNIVERSE, review.get("target_universe")),
        "corporate_action_authority_created_true": (True, review.get("corporate_action_authority_created")),
        "corporate_action_authority_approved_true": (True, review.get("corporate_action_authority_approved")),
        "corporate_action_authority_scope_corporate_action_only": (candidate_service.authority.CORPORATE_ACTION_AUTHORITY_ONLY, review.get("corporate_action_authority_scope")),
        "split_event_authority_created_true": (True, review.get("split_event_authority_created")),
        "split_event_authority_frozen_true": (True, review.get("split_event_authority_frozen")),
        "dividend_event_authority_created_true": (True, review.get("dividend_event_authority_created")),
        "dividend_event_authority_frozen_true": (True, review.get("dividend_event_authority_frozen")),
        "ready_for_acquisition_generation_chain_candidate_true": (True, review.get("ready_for_acquisition_generation_chain_candidate")),
        "acquisition_generation_chain_candidate_created_true": (True, review.get("acquisition_generation_chain_candidate_created")),
        "acquisition_generation_chain_review_created_true": (True, review.get("acquisition_generation_chain_candidate_review_created")),
        "acquisition_chain_scope_candidate_only": (candidate_service.ACQUISITION_GENERATION_CHAIN_SCOPE, review.get("acquisition_generation_chain_scope")),
        "acquisition_generation_authority_status_not_authorized": (candidate_service.ACQUISITION_GENERATION_AUTHORITY_STATUS, review.get("acquisition_generation_authority_status")),
        "per_ticker_acquisition_chain_entries_12": (12, review.get("reviewed_per_ticker_acquisition_generation_chain_candidate_entry_count")),
        "per_ticker_acquisition_chain_review_entries_12": (12, len(entries)),
        "per_ticker_acquisition_chain_candidate_digests_present": (True, len(entries) == 12 and all(isinstance(row.get("per_ticker_acquisition_generation_chain_candidate_digest"), str) and len(row["per_ticker_acquisition_generation_chain_candidate_digest"]) == 64 for row in entries)),
        "per_ticker_acquisition_chain_review_digests_present": (True, len(entries) == 12 and all(isinstance(row.get("per_ticker_acquisition_generation_chain_review_digest"), str) and len(row["per_ticker_acquisition_generation_chain_review_digest"]) == 64 for row in entries)),
        "acquisition_planning_dimensions_reviewed": (candidate_service.ACQUISITION_PLANNING_DIMENSIONS, review.get("acquisition_planning_dimensions")),
        "future_acquisition_chain_reviewed": (candidate_service.FUTURE_ACQUISITION_CHAIN, review.get("future_acquisition_chain")),
        "future_provider_request_policy_reviewed": (candidate_service.FUTURE_ACQUISITION_PROVIDER_REQUEST_POLICY, review.get("future_acquisition_provider_request_policy")),
        "future_gates_defined": (candidate_service.FUTURE_GATES, review.get("future_gates")),
        "risk_controls_defined": (candidate_service.RISK_CONTROLS, review.get("risk_controls")),
        "planned_outputs_9": (9, review.get("planned_output_count")),
        "planned_outputs_not_generated": (True, len(outputs) == 9 and all(row.get("generation_status") == candidate_service.PLANNED_NOT_GENERATED for row in outputs)),
        "planned_outputs_research_only": (True, len(outputs) == 9 and all(row.get("actionability") == candidate_service.RESEARCH_ONLY_NON_ACTIONABLE for row in outputs)),
        "predictive_usefulness_not_accepted": (candidate_service.NOT_ACCEPTED, review.get("predictive_usefulness")),
        "profitability_not_accepted": (candidate_service.PROFITABILITY_NOT_ACCEPTED, review.get("profitability")),
        "runtime_use_not_authorized": (candidate_service.NOT_AUTHORIZED, review.get("runtime_use")),
        "strategy_use_not_authorized": (candidate_service.NOT_AUTHORIZED, review.get("strategy_use")),
        "paper_trading_not_authorized": (candidate_service.NOT_AUTHORIZED, review.get("paper_trading")),
        "broker_execution_not_authorized": (candidate_service.NOT_AUTHORIZED, review.get("broker_execution")),
    }
    false_checks = {
        "provider_requests_made_in_review_false": "provider_requests_made_in_review",
        "live_provider_transport_enabled_in_review_false": "live_provider_transport_enabled_in_review",
        "market_data_acquisition_performed_in_review_false": "market_data_acquisition_performed_in_review",
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
        "no_acquisition_authorization_artifact_created": "acquisition_authorization_artifact_created",
        "no_acquisition_execution_artifact_created": "acquisition_execution_artifact_created",
        "no_dataset_generation_authorization_created": "dataset_generation_authorization_created",
        "no_canonical_dataset_artifact_created": "canonical_dataset_artifact_created",
        "no_registry_approval_created": "registry_approval_artifact_created",
        "no_predictive_usefulness_acceptance_artifact_created": "predictive_usefulness_acceptance_artifact_created",
        "no_profitability_acceptance_created": "profitability_acceptance_created",
        "no_runtime_migration_approval_created": "runtime_migration_approval_created",
    }
    values.update(
        {check_id: (False, review.get(field)) for check_id, field in false_checks.items()}
    )
    return [_check(check_id, *values[check_id]) for check_id in REQUIRED_CHECK_IDS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [row for row in checklist if row["status"] != PASS]
    return {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row["severity"] == BLOCKER for row in failed),
        "ready_for_operator_assessment": not failed,
        "ready_for_acquisition_provider_request_approval": False,
        "ready_for_acquisition_generation_approval": False,
        "ready_for_acquisition_generation_freeze": False,
        "ready_for_canonical_dataset_chain_candidate": False,
        "acquisition_authorized": False,
        "dataset_generation_authorized": False,
        "canonical_dataset_authorized": False,
        "registry_approval_created": False,
        "additional_predictive_evidence_execution_authorized": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def acquisition_generation_chain_candidate_review_package_digest_v1(
    review_package: dict[str, Any],
) -> str:
    payload = deepcopy(review_package)
    payload.pop("acquisition_generation_chain_candidate_review_package_digest", None)
    return semantic_digest(payload)


def build_acquisition_generation_chain_candidate_review_package_v1(
    candidate: dict[str, Any] | None = None,
) -> dict[str, Any]:
    source, binding_mode = _candidate_for_binding(candidate)
    review = _base_review_package(source, binding_mode)
    review["review_checklist"] = _review_checklist(review)
    review["review_summary"] = _summary(review["review_checklist"])
    review["acquisition_generation_chain_candidate_review_package_digest"] = (
        acquisition_generation_chain_candidate_review_package_digest_v1(review)
    )
    validate_acquisition_generation_chain_candidate_review_package_v1(review)
    return review


def _validate_per_ticker(review: dict[str, Any]) -> None:
    entries = review.get("per_ticker_acquisition_generation_chain_review_entries")
    if not isinstance(entries, list) or len(entries) != 12:
        raise AcquisitionGenerationChainCandidateReviewPackageError(
            "per_ticker review entries mismatch"
        )
    _expect([row.get("ticker") for row in entries], TARGET_UNIVERSE, "per_ticker tickers")
    expected = {
        row["ticker"]: row for row in candidate_service._per_ticker_entries()
    }
    for row in entries:
        source = expected[row["ticker"]]
        for field, value in source.items():
            _expect(row.get(field), value, f"{row['ticker']}.{field}")
        _expect(
            row.get("acquisition_generation_chain_review_status"),
            READY_FOR_OPERATOR_ASSESSMENT,
            f"{row['ticker']}.review status",
        )
        _expect(
            row.get("source_acquisition_generation_chain_candidate_digest"),
            EXPECTED_REVIEWED_ACQUISITION_GENERATION_CHAIN_CANDIDATE_DIGEST,
            f"{row['ticker']}.source candidate digest",
        )
        digest = row.get("per_ticker_acquisition_generation_chain_review_digest")
        _expect_digest(digest, f"{row['ticker']}.review digest")
        _expect(
            digest,
            per_ticker_acquisition_generation_chain_review_digest_v1(row),
            f"{row['ticker']}.review digest",
        )


def validate_acquisition_generation_chain_candidate_review_package_v1(
    review_package: dict[str, Any],
) -> dict[str, Any]:
    if not isinstance(review_package, dict):
        raise AcquisitionGenerationChainCandidateReviewPackageError(
            "review_package must be an object"
        )
    expected = {
        "artifact_kind": ARTIFACT_KIND_ACQUISITION_GENERATION_CHAIN_CANDIDATE_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_ACQUISITION_GENERATION_CHAIN_CANDIDATE_REVIEW_V1,
        "review_status": ACQUISITION_GENERATION_CHAIN_CANDIDATE_REVIEW_PACKAGE_READY,
        "reviewed_acquisition_generation_chain_candidate_kind": candidate_service.ARTIFACT_KIND_ACQUISITION_GENERATION_CHAIN_CANDIDATE,
        "reviewed_acquisition_generation_chain_candidate_status": candidate_service.ACQUISITION_GENERATION_CHAIN_READY_FOR_OPERATOR_REVIEW,
        "reviewed_acquisition_generation_chain_candidate_digest": EXPECTED_REVIEWED_ACQUISITION_GENERATION_CHAIN_CANDIDATE_DIGEST,
        "reviewed_acquisition_generation_chain_candidate_checklist_total": EXPECTED_REVIEWED_CANDIDATE_CHECKLIST_TOTAL,
        "reviewed_acquisition_generation_chain_candidate_checklist_passed": EXPECTED_REVIEWED_CANDIDATE_CHECKLIST_PASSED,
        "reviewed_acquisition_generation_chain_candidate_checklist_failed": EXPECTED_REVIEWED_CANDIDATE_CHECKLIST_FAILED,
        "reviewed_acquisition_generation_chain_candidate_blocker_count": EXPECTED_REVIEWED_CANDIDATE_BLOCKER_COUNT,
        "corporate_action_authority_approval_digest": candidate_service.EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST,
        "combined_split_dividend_corporate_action_readiness_review_package_digest": candidate_service.EXPECTED_COMBINED_READINESS_REVIEW_PACKAGE_DIGEST,
        "split_event_authority_freeze_digest": candidate_service.EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST,
        "dividend_event_authority_freeze_digest": candidate_service.EXPECTED_DIVIDEND_EVENT_AUTHORITY_FREEZE_DIGEST,
        "identity_authority_freeze_digest": candidate_service.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
        "target_universe_count": 12,
        "target_universe": TARGET_UNIVERSE,
        "corporate_action_authority_scope": candidate_service.authority.CORPORATE_ACTION_AUTHORITY_ONLY,
        "acquisition_generation_chain_objective": candidate_service.ACQUISITION_GENERATION_CHAIN_OBJECTIVE,
        "acquisition_generation_chain_scope": candidate_service.ACQUISITION_GENERATION_CHAIN_SCOPE,
        "acquisition_generation_mode": candidate_service.ACQUISITION_GENERATION_MODE,
        "acquisition_generation_authority_status": candidate_service.ACQUISITION_GENERATION_AUTHORITY_STATUS,
        "acquisition_planning_dimensions": candidate_service.ACQUISITION_PLANNING_DIMENSIONS,
        "future_acquisition_provider_request_policy": candidate_service.FUTURE_ACQUISITION_PROVIDER_REQUEST_POLICY,
        "future_acquisition_chain": candidate_service.FUTURE_ACQUISITION_CHAIN,
        "future_gates": candidate_service.FUTURE_GATES,
        "risk_controls": candidate_service.RISK_CONTROLS,
        "planned_output_count": 9,
        "planned_outputs_status": candidate_service.PLANNED_NOT_GENERATED,
        "planned_outputs_label": candidate_service.RESEARCH_ONLY_NON_ACTIONABLE,
        "predictive_usefulness": candidate_service.NOT_ACCEPTED,
        "profitability": candidate_service.PROFITABILITY_NOT_ACCEPTED,
        "runtime_use": candidate_service.NOT_AUTHORIZED,
        "strategy_use": candidate_service.NOT_AUTHORIZED,
        "paper_trading": candidate_service.NOT_AUTHORIZED,
        "broker_execution": candidate_service.NOT_AUTHORIZED,
    }
    for field, value in expected.items():
        _expect(review_package.get(field), value, field)
    true_fields = (
        "created_offline",
        "acquisition_generation_chain_candidate_created",
        "acquisition_generation_chain_candidate_review_created",
        "acquisition_generation_chain_ready_for_operator_review",
        "ready_for_acquisition_generation_chain_candidate",
        "corporate_action_authority_created",
        "corporate_action_authority_approved",
        "split_event_authority_created",
        "split_event_authority_frozen",
        "dividend_event_authority_created",
        "dividend_event_authority_frozen",
        "identity_authority_created",
        "identity_authority_frozen",
        "research_only",
        "operator_review_required",
    )
    false_fields = (
        "provider_requests_made_in_review",
        "live_provider_transport_enabled_in_review",
        "market_data_acquisition_performed_in_review",
        "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
        "acquisition_generation_chain_approved",
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
        "acquisition_authorization_artifact_created",
        "acquisition_execution_artifact_created",
        "dataset_generation_authorization_created",
        "canonical_dataset_artifact_created",
        "registry_approval_artifact_created",
        "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_created",
        "runtime_migration_approval_created",
    )
    for field in true_fields:
        _expect_true(review_package.get(field), field)
    for field in false_fields:
        _expect_false(review_package.get(field), field)
    outputs = review_package.get("planned_outputs")
    if not isinstance(outputs, list) or len(outputs) != 9:
        raise AcquisitionGenerationChainCandidateReviewPackageError(
            "planned_outputs mismatch"
        )
    if any(
        row.get("generation_status") != candidate_service.PLANNED_NOT_GENERATED
        for row in outputs
    ):
        raise AcquisitionGenerationChainCandidateReviewPackageError(
            "planned output generated"
        )
    if any(
        row.get("actionability") != candidate_service.RESEARCH_ONLY_NON_ACTIONABLE
        for row in outputs
    ):
        raise AcquisitionGenerationChainCandidateReviewPackageError(
            "planned output actionable"
        )
    _validate_per_ticker(review_package)
    checklist = review_package.get("review_checklist")
    if not isinstance(checklist, list):
        raise AcquisitionGenerationChainCandidateReviewPackageError(
            "review_checklist missing"
        )
    _expect(
        [row.get("check_id") for row in checklist],
        REQUIRED_CHECK_IDS,
        "review checklist",
    )
    if any(row.get("status") != PASS for row in checklist):
        raise AcquisitionGenerationChainCandidateReviewPackageError(
            "review checklist failed"
        )
    _expect(review_package.get("review_summary"), _summary(checklist), "review_summary")
    digest = review_package.get(
        "acquisition_generation_chain_candidate_review_package_digest"
    )
    _expect_digest(digest, "review package digest")
    _expect(
        digest,
        acquisition_generation_chain_candidate_review_package_digest_v1(
            review_package
        ),
        "review package digest",
    )
    return {
        "status": "ACQUISITION_GENERATION_CHAIN_CANDIDATE_REVIEW_PACKAGE_VALID",
        "artifact_kind": review_package["artifact_kind"],
        "review_status": review_package["review_status"],
        "acquisition_generation_chain_candidate_review_package_digest": digest,
        **{
            key: review_package["review_summary"][key]
            for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")
        },
    }


def build_acquisition_generation_chain_candidate_review_markdown_v1(
    review_package: dict[str, Any],
) -> str:
    validation = validate_acquisition_generation_chain_candidate_review_package_v1(
        review_package
    )
    lines = [
        "# MarketFlow Acquisition Generation Chain Candidate Operator Review Status",
        "",
        "## Title",
        "- Acquisition Generation Chain Candidate Operator Review Package v1.",
        "",
        "## Acquisition Generation Chain Candidate Review Package",
        f"- Artifact/status: `{review_package['artifact_kind']}` / `{review_package['review_status']}`.",
        f"- Digest: `{validation['acquisition_generation_chain_candidate_review_package_digest']}`.",
        "",
        "## Reviewed Candidate",
        f"- Candidate digest: `{review_package['reviewed_acquisition_generation_chain_candidate_digest']}`.",
        "",
        "## Source Corporate-Action Authority Approval",
        f"- Approval digest: `{review_package['corporate_action_authority_approval_digest']}`.",
        "",
        "## Target Universe",
        "- " + ", ".join(f"`{ticker}`" for ticker in TARGET_UNIVERSE),
        "",
        "## Per-Ticker Acquisition Chain Review Entries",
    ]
    lines.extend(
        f"- `{row['ticker']}`: `{row['acquisition_generation_chain_review_status']}`; acquisition `{row['market_data_acquisition_status']}`."
        for row in review_package[
            "per_ticker_acquisition_generation_chain_review_entries"
        ]
    )
    lines.extend(["", "## Acquisition Planning Dimensions"])
    lines.extend(
        f"- `{item}`." for item in review_package["acquisition_planning_dimensions"]
    )
    lines.extend(["", "## Future Provider Request Policy"])
    lines.extend(
        f"- `{key}`: `{value}`."
        for key, value in review_package[
            "future_acquisition_provider_request_policy"
        ].items()
    )
    lines.extend(["", "## Future Acquisition Chain"])
    lines.extend(
        f"{index}. {item}"
        for index, item in enumerate(
            review_package["future_acquisition_chain"], start=1
        )
    )
    lines.extend(["", "## Future Gates"])
    lines.extend(f"- `{item}`." for item in review_package["future_gates"])
    lines.extend(["", "## Risk Controls"])
    lines.extend(f"- `{item}`." for item in review_package["risk_controls"])
    lines.extend(
        [
            "",
            "## Acquisition Boundary",
            "- Review only; acquisition is neither authorized nor executed.",
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
            "## Checklist Summary",
            f"- Total/passed/failed/blockers: `{validation['total_checks']} / {validation['passed_checks']} / {validation['failed_checks']} / {validation['blocker_count']}`.",
            "",
            "## Guardrails",
            "- No provider request, acquisition, dataset generation, predictive execution, or runtime activation occurred.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_acquisition_generation_chain_candidate_review_package_v1(
    output_dir: str | Path,
    *,
    candidate: dict[str, Any] | None = None,
) -> dict[str, Any]:
    review = build_acquisition_generation_chain_candidate_review_package_v1(candidate)
    output_path = Path(output_dir)
    json_path = (
        output_path / "acquisition_generation_chain_candidate_review_package_v1.json"
    )
    markdown_path = (
        output_path / "acquisition_generation_chain_candidate_review_package_v1.md"
    )
    if json_path.exists() or markdown_path.exists():
        raise AcquisitionGenerationChainCandidateReviewPackageError(
            "acquisition-generation candidate review output already exists"
        )
    output_path.mkdir(parents=True, exist_ok=True)
    json_path.write_bytes(canonical_json_bytes(review))
    markdown_path.write_text(
        build_acquisition_generation_chain_candidate_review_markdown_v1(review),
        encoding="utf-8",
    )
    return {
        "review_package": review,
        "validation": validate_acquisition_generation_chain_candidate_review_package_v1(
            review
        ),
        "json_path": json_path.as_posix(),
        "markdown_path": markdown_path.as_posix(),
    }
