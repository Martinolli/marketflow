"""Offline operator review package for the split-event authority candidate."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import split_event_authority_candidate_service as candidate_service


ARTIFACT_KIND_SPLIT_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE = (
    "SPLIT_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE"
)
SCHEMA_VERSION_SPLIT_EVENT_AUTHORITY_CANDIDATE_REVIEW_V1 = (
    "split_event_authority_candidate_review_v1"
)
SPLIT_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_READY = (
    "SPLIT_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_READY"
)
SPLIT_EVENT_AUTHORITY_CANDIDATE_STATUS_BINDING = (
    "SPLIT_EVENT_AUTHORITY_CANDIDATE_STATUS_BINDING"
)
SPLIT_EVENT_AUTHORITY_CANDIDATE_OBJECT_BINDING = (
    "SPLIT_EVENT_AUTHORITY_CANDIDATE_OBJECT_BINDING"
)

EXPECTED_REVIEWED_SPLIT_EVENT_AUTHORITY_CANDIDATE_DIGEST = (
    "7faaaaf19f0630f200c7decaafc2555ea23dab3bcfdffd17713487f33d5d8e0b"
)
EXPECTED_REVIEWED_SPLIT_EVENT_AUTHORITY_CANDIDATE_CHECKLIST_TOTAL = len(
    candidate_service.REQUIRED_CHECK_IDS
)
EXPECTED_REVIEWED_SPLIT_EVENT_AUTHORITY_CANDIDATE_CHECKLIST_PASSED = len(
    candidate_service.REQUIRED_CHECK_IDS
)
EXPECTED_REVIEWED_SPLIT_EVENT_AUTHORITY_CANDIDATE_CHECKLIST_FAILED = 0
EXPECTED_REVIEWED_SPLIT_EVENT_AUTHORITY_CANDIDATE_BLOCKER_COUNT = 0

READY_FOR_OPERATOR_ASSESSMENT = "READY_FOR_OPERATOR_ASSESSMENT"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

VALIDATION_TARGET_UNIVERSE = list(candidate_service.VALIDATION_TARGET_UNIVERSE)
SPLIT_EVENT_EVIDENCE_REQUIREMENTS = list(
    candidate_service.SPLIT_EVENT_EVIDENCE_REQUIREMENTS
)
SPLIT_EVENT_EVIDENCE_REQUIREMENT_POLICY = deepcopy(
    candidate_service.SPLIT_EVENT_EVIDENCE_REQUIREMENT_POLICY
)
FUTURE_SPLIT_PROVIDER_REQUEST_POLICY = deepcopy(
    candidate_service.FUTURE_SPLIT_PROVIDER_REQUEST_POLICY
)
FUTURE_SPLIT_AUTHORITY_CHAIN = list(candidate_service.FUTURE_SPLIT_AUTHORITY_CHAIN)
FUTURE_CORPORATE_ACTION_READINESS_CHAIN = list(
    candidate_service.FUTURE_CORPORATE_ACTION_READINESS_CHAIN
)
FUTURE_GATES = list(candidate_service.FUTURE_GATES)
RISK_CONTROLS = list(candidate_service.RISK_CONTROLS)

PLANNED_REVIEW_OUTPUT_NAMES = [
    "split_provider_evidence_request_approval_ceremony",
    "split_provider_evidence_execution",
    "split_event_evidence_results_review_package",
    "split_event_authority_candidate_update_or_discrepancy_triage",
    "split_event_authority_freeze_ceremony",
    "dividend_event_authority_candidate",
    "combined_corporate_action_readiness_review",
    "acquisition_generation_chain_candidate_after_corporate_action_authority",
]

REQUIRED_CHECK_IDS = [
    "reviewed_split_event_candidate_kind_matches",
    "reviewed_split_event_candidate_status_ready",
    "reviewed_split_event_candidate_digest_matches",
    "reviewed_split_event_candidate_checklist_zero_blockers",
    "split_event_candidate_digest_bound",
    "corporate_action_plan_approval_digest_bound",
    "corporate_action_plan_review_digest_bound",
    "corporate_action_plan_candidate_digest_bound",
    "registry_inventory_approval_digest_bound",
    "registry_inventory_review_digest_bound",
    "registry_inventory_candidate_digest_bound",
    "identity_freeze_digest_bound",
    "identity_candidate_review_digest_bound",
    "identity_candidate_digest_bound",
    "live_validation_results_review_digest_bound",
    "live_validation_execution_digest_bound",
    "ticker_universe_selection_approval_digest_bound",
    "target_universe_count_12",
    "target_universe_matches_split_candidate_universe",
    "identity_authority_frozen_true",
    "registry_inventory_approved_true",
    "corporate_action_plan_approved_true",
    "ready_for_split_event_authority_candidate_true",
    "split_event_candidate_objective_reviewed",
    "split_event_candidate_scope_candidate_only",
    "split_event_authority_creation_status_not_created",
    "split_event_authority_freeze_status_not_frozen",
    "per_ticker_split_event_candidate_entries_12",
    "per_ticker_split_event_review_entries_12",
    "per_ticker_split_event_candidate_status_ready",
    "per_ticker_split_event_review_status_ready",
    "per_ticker_split_event_authority_not_created",
    "per_ticker_split_event_freeze_not_frozen",
    "per_ticker_provider_evidence_request_not_authorized",
    "per_ticker_provider_evidence_execution_not_executed",
    "per_ticker_split_history_not_fetched",
    "per_ticker_split_event_candidate_digests_present",
    "per_ticker_split_event_review_digests_present",
    "split_event_evidence_requirements_reviewed",
    "split_event_evidence_requirement_policy_reviewed",
    "future_split_provider_request_policy_reviewed",
    "future_split_authority_chain_reviewed",
    "future_corporate_action_readiness_chain_reviewed",
    "future_gates_defined",
    "risk_controls_defined",
    "planned_outputs_8",
    "planned_outputs_not_generated",
    "planned_outputs_research_only",
    "provider_requests_made_in_review_false",
    "live_validation_rerun_performed_false",
    "live_provider_transport_enabled_in_review_false",
    "split_event_authority_candidate_created_false",
    "split_event_authority_review_created_true",
    "split_event_authority_created_false",
    "split_event_authority_frozen_false",
    "split_provider_evidence_request_authorized_false",
    "split_provider_evidence_executed_false",
    "split_provider_evidence_results_created_false",
    "dividend_event_authority_candidate_created_false",
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
    "no_split_event_authority_artifact_created",
    "no_split_event_authority_freeze_created",
    "no_split_provider_evidence_request_approval_created",
    "no_split_provider_evidence_execution_created",
    "no_dividend_event_authority_artifact_created",
    "no_corporate_action_authority_artifact_created",
    "no_acquisition_authorization_created",
    "no_dataset_generation_authorization_created",
    "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created",
    "no_runtime_migration_approval_created",
]


class SplitEventAuthorityCandidateReviewPackageError(ValueError):
    """Raised when the split-event authority candidate review package is invalid."""


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
        raise SplitEventAuthorityCandidateReviewPackageError(f"{field_name} mismatch")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise SplitEventAuthorityCandidateReviewPackageError(
            f"{field_name} must be true"
        )


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise SplitEventAuthorityCandidateReviewPackageError(
            f"{field_name} must be false"
        )


def _not_authorized() -> str:
    return candidate_service.NOT_AUTHORIZED


def _path_text(path: Path) -> str:
    return str(path).replace("\\", "/")


def _candidate_for_binding(
    candidate: dict[str, Any] | None,
) -> tuple[dict[str, Any], str]:
    if candidate is None:
        return (
            candidate_service.build_split_event_authority_candidate_v1(),
            SPLIT_EVENT_AUTHORITY_CANDIDATE_STATUS_BINDING,
        )
    candidate_service.validate_split_event_authority_candidate_v1(candidate)
    return deepcopy(candidate), SPLIT_EVENT_AUTHORITY_CANDIDATE_OBJECT_BINDING


def _per_ticker_review_digest_payload(entry: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(entry)
    payload.pop("per_ticker_split_event_review_digest", None)
    return payload


def per_ticker_split_event_review_digest_v1(entry: dict[str, Any]) -> str:
    """Return the deterministic semantic digest for one per-ticker review entry."""
    return semantic_digest(_per_ticker_review_digest_payload(entry))


def _review_entries(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for source in candidate.get("per_ticker_split_event_candidate_entries", []):
        entry = deepcopy(source)
        entry["split_event_review_status"] = READY_FOR_OPERATOR_ASSESSMENT
        entry["per_ticker_split_event_review_digest"] = (
            per_ticker_split_event_review_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _candidate_entry_from_review_entry(entry: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(entry)
    payload.pop("split_event_review_status", None)
    payload.pop("per_ticker_split_event_review_digest", None)
    return payload


def _planned_outputs() -> list[dict[str, Any]]:
    return [
        {
            "output_name": output_name,
            "generation_status": candidate_service.PLANNED_NOT_GENERATED,
            "generated": False,
            "actionability": candidate_service.RESEARCH_ONLY_NON_ACTIONABLE,
        }
        for output_name in PLANNED_REVIEW_OUTPUT_NAMES
    ]


def _base_review_package(
    candidate: dict[str, Any], binding_mode: str
) -> dict[str, Any]:
    summary = candidate["candidate_summary"]
    return {
        "artifact_kind": ARTIFACT_KIND_SPLIT_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_SPLIT_EVENT_AUTHORITY_CANDIDATE_REVIEW_V1,
        "review_status": SPLIT_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_READY,
        "split_event_authority_candidate_binding_mode": binding_mode,
        "created_offline": True,
        "provider_requests_made_in_review": False,
        "live_validation_rerun_performed": False,
        "live_provider_transport_enabled_in_review": False,
        "split_event_authority_candidate_created": False,
        "split_event_authority_review_created": True,
        "split_event_authority_created": False,
        "split_event_authority_frozen": False,
        "split_event_authority_artifact_created": False,
        "split_event_authority_freeze_created": False,
        "split_provider_evidence_request_authorized": False,
        "split_provider_evidence_executed": False,
        "split_provider_evidence_results_created": False,
        "split_provider_evidence_request_approval_created": False,
        "split_provider_evidence_execution_created": False,
        "corporate_action_authority_plan_approved": True,
        "corporate_action_authority_created": False,
        "corporate_action_authority_artifact_created": False,
        "ready_for_split_event_authority_candidate": True,
        "ready_for_dividend_event_authority_candidate": True,
        "ready_for_split_event_provider_evidence_request_approval": False,
        "ready_for_split_event_authority_freeze": False,
        "dividend_event_authority_candidate_created": False,
        "dividend_event_authority_review_created": False,
        "dividend_event_authority_created": False,
        "dividend_event_authority_frozen": False,
        "dividend_event_authority_artifact_created": False,
        "dividend_provider_evidence_request_authorized": False,
        "dividend_provider_evidence_executed": False,
        "post_identity_freeze_registry_inventory_approved": True,
        "identity_authority_created": True,
        "identity_authority_frozen": True,
        "new_ticker_identity_authority_created": True,
        "authority_scope": candidate["authority_scope"],
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
        "runtime_use": candidate["runtime_use"],
        "strategy_use": candidate["strategy_use"],
        "paper_trading": candidate["paper_trading"],
        "broker_execution": candidate["broker_execution"],
        "automatic_stitching": False,
        "operator_review_required": True,
        "reviewed_split_event_authority_candidate_kind": candidate["artifact_kind"],
        "reviewed_split_event_authority_candidate_status": candidate["candidate_status"],
        "reviewed_split_event_authority_candidate_digest": candidate[
            "split_event_authority_candidate_digest"
        ],
        "reviewed_split_event_authority_candidate_checklist_total": summary[
            "total_checks"
        ],
        "reviewed_split_event_authority_candidate_checklist_passed": summary[
            "passed_checks"
        ],
        "reviewed_split_event_authority_candidate_checklist_failed": summary[
            "failed_checks"
        ],
        "reviewed_split_event_authority_candidate_blocker_count": summary[
            "blocker_count"
        ],
        "split_event_authority_candidate_digest": candidate[
            "split_event_authority_candidate_digest"
        ],
        "source_corporate_action_plan_approval_kind": candidate[
            "source_corporate_action_plan_approval_kind"
        ],
        "source_corporate_action_plan_approval_status": candidate[
            "source_corporate_action_plan_approval_status"
        ],
        "source_corporate_action_plan_approval_scope": candidate[
            "source_corporate_action_plan_approval_scope"
        ],
        "corporate_action_authority_plan_approval_digest": candidate[
            "corporate_action_authority_plan_approval_digest"
        ],
        "corporate_action_authority_plan_candidate_review_package_digest": candidate[
            "corporate_action_authority_plan_candidate_review_package_digest"
        ],
        "corporate_action_authority_plan_candidate_digest": candidate[
            "corporate_action_authority_plan_candidate_digest"
        ],
        "post_identity_freeze_registry_inventory_approval_digest": candidate[
            "post_identity_freeze_registry_inventory_approval_digest"
        ],
        "post_identity_freeze_registry_inventory_candidate_review_package_digest": candidate[
            "post_identity_freeze_registry_inventory_candidate_review_package_digest"
        ],
        "post_identity_freeze_registry_inventory_candidate_digest": candidate[
            "post_identity_freeze_registry_inventory_candidate_digest"
        ],
        "identity_authority_freeze_digest": candidate["identity_authority_freeze_digest"],
        "identity_authority_candidate_review_package_digest": candidate[
            "identity_authority_candidate_review_package_digest"
        ],
        "identity_authority_candidate_digest": candidate[
            "identity_authority_candidate_digest"
        ],
        "live_ticker_validation_results_review_package_digest": candidate[
            "live_ticker_validation_results_review_package_digest"
        ],
        "live_ticker_validation_execution_digest": candidate[
            "live_ticker_validation_execution_digest"
        ],
        "ticker_universe_selection_approval_digest": candidate[
            "ticker_universe_selection_approval_digest"
        ],
        "target_universe": list(candidate["target_universe"]),
        "corporate_action_plan_universe": list(candidate["corporate_action_plan_universe"]),
        "target_universe_count": candidate["target_universe_count"],
        "split_event_authority_candidate_objective": candidate[
            "split_event_authority_candidate_objective"
        ],
        "split_event_authority_candidate_scope": candidate[
            "split_event_authority_candidate_scope"
        ],
        "split_event_authority_creation_status": candidate[
            "split_event_authority_creation_status"
        ],
        "split_event_authority_freeze_status": candidate[
            "split_event_authority_freeze_status"
        ],
        "per_ticker_split_event_candidate_entries": deepcopy(
            candidate["per_ticker_split_event_candidate_entries"]
        ),
        "per_ticker_split_event_review_entries": _review_entries(candidate),
        "split_event_evidence_requirements": list(
            candidate["split_event_evidence_requirements"]
        ),
        "split_event_evidence_requirement_policy": deepcopy(
            candidate["split_event_evidence_requirement_policy"]
        ),
        "future_split_provider_request_policy": deepcopy(
            candidate["future_split_provider_request_policy"]
        ),
        "future_split_authority_chain": list(candidate["future_split_authority_chain"]),
        "future_corporate_action_readiness_chain": list(
            candidate["future_corporate_action_readiness_chain"]
        ),
        "future_gates": list(candidate["future_gates"]),
        "risk_controls": list(candidate["risk_controls"]),
        "planned_outputs": _planned_outputs(),
        "planned_output_count": len(PLANNED_REVIEW_OUTPUT_NAMES),
        "planned_outputs_status": candidate_service.PLANNED_NOT_GENERATED,
        "planned_outputs_label": candidate_service.RESEARCH_ONLY_NON_ACTIONABLE,
        "acquisition_authorization_created": False,
        "dataset_generation_authorization_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
    }


def _entries(review_package: dict[str, Any]) -> list[dict[str, Any]]:
    entries = review_package.get("per_ticker_split_event_candidate_entries")
    return entries if isinstance(entries, list) else []


def _review_entries_from_package(
    review_package: dict[str, Any]
) -> list[dict[str, Any]]:
    entries = review_package.get("per_ticker_split_event_review_entries")
    return entries if isinstance(entries, list) else []


def _digests_present(entries: list[dict[str, Any]], field_name: str) -> bool:
    return all(
        isinstance(entry.get(field_name), str) and len(entry[field_name]) == 64
        for entry in entries
    )


def _all_entry_field(
    entries: list[dict[str, Any]], field_name: str, expected: Any
) -> bool:
    return len(entries) == 12 and all(
        entry.get(field_name) == expected for entry in entries
    )


def _planned_outputs_not_generated(review_package: dict[str, Any]) -> bool:
    outputs = review_package.get("planned_outputs")
    return isinstance(outputs, list) and bool(outputs) and all(
        output.get("generation_status") == candidate_service.PLANNED_NOT_GENERATED
        and output.get("generated") is False
        for output in outputs
    )


def _planned_outputs_research_only(review_package: dict[str, Any]) -> bool:
    outputs = review_package.get("planned_outputs")
    return isinstance(outputs, list) and bool(outputs) and all(
        output.get("actionability") == candidate_service.RESEARCH_ONLY_NON_ACTIONABLE
        for output in outputs
    )


def _checklist(review_package: dict[str, Any]) -> list[dict[str, Any]]:
    entries = _entries(review_package)
    review_entries = _review_entries_from_package(review_package)
    return [
        _check("reviewed_split_event_candidate_kind_matches", candidate_service.ARTIFACT_KIND_SPLIT_EVENT_AUTHORITY_CANDIDATE, review_package.get("reviewed_split_event_authority_candidate_kind")),
        _check("reviewed_split_event_candidate_status_ready", candidate_service.SPLIT_EVENT_AUTHORITY_READY_FOR_OPERATOR_REVIEW, review_package.get("reviewed_split_event_authority_candidate_status")),
        _check("reviewed_split_event_candidate_digest_matches", EXPECTED_REVIEWED_SPLIT_EVENT_AUTHORITY_CANDIDATE_DIGEST, review_package.get("reviewed_split_event_authority_candidate_digest")),
        _check("reviewed_split_event_candidate_checklist_zero_blockers", 0, review_package.get("reviewed_split_event_authority_candidate_blocker_count")),
        _check("split_event_candidate_digest_bound", EXPECTED_REVIEWED_SPLIT_EVENT_AUTHORITY_CANDIDATE_DIGEST, review_package.get("split_event_authority_candidate_digest")),
        _check("corporate_action_plan_approval_digest_bound", candidate_service.EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST, review_package.get("corporate_action_authority_plan_approval_digest")),
        _check("corporate_action_plan_review_digest_bound", candidate_service.EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST, review_package.get("corporate_action_authority_plan_candidate_review_package_digest")),
        _check("corporate_action_plan_candidate_digest_bound", candidate_service.EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_DIGEST, review_package.get("corporate_action_authority_plan_candidate_digest")),
        _check("registry_inventory_approval_digest_bound", candidate_service.approval.review.plan.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST, review_package.get("post_identity_freeze_registry_inventory_approval_digest")),
        _check("registry_inventory_review_digest_bound", candidate_service.approval.review.plan.approval_service.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_REVIEW_PACKAGE_DIGEST, review_package.get("post_identity_freeze_registry_inventory_candidate_review_package_digest")),
        _check("registry_inventory_candidate_digest_bound", candidate_service.approval.review.plan.approval_service.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_DIGEST, review_package.get("post_identity_freeze_registry_inventory_candidate_digest")),
        _check("identity_freeze_digest_bound", candidate_service.approval.review.plan.approval_service.review_service.candidate_service.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST, review_package.get("identity_authority_freeze_digest")),
        _check("identity_candidate_review_digest_bound", candidate_service.approval.review.plan.approval_service.review_service.candidate_service.freeze_service.EXPECTED_IDENTITY_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST, review_package.get("identity_authority_candidate_review_package_digest")),
        _check("identity_candidate_digest_bound", candidate_service.approval.review.plan.approval_service.review_service.candidate_service.freeze_service.EXPECTED_IDENTITY_AUTHORITY_CANDIDATE_DIGEST, review_package.get("identity_authority_candidate_digest")),
        _check("live_validation_results_review_digest_bound", candidate_service.approval.review.plan.approval_service.review_service.candidate_service.freeze_service.EXPECTED_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_DIGEST, review_package.get("live_ticker_validation_results_review_package_digest")),
        _check("live_validation_execution_digest_bound", candidate_service.approval.review.plan.approval_service.review_service.candidate_service.freeze_service.EXPECTED_LIVE_TICKER_VALIDATION_EXECUTION_DIGEST, review_package.get("live_ticker_validation_execution_digest")),
        _check("ticker_universe_selection_approval_digest_bound", candidate_service.approval.review.plan.approval_service.review_service.candidate_service.freeze_service.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST, review_package.get("ticker_universe_selection_approval_digest")),
        _check("target_universe_count_12", 12, review_package.get("target_universe_count")),
        _check("target_universe_matches_split_candidate_universe", True, review_package.get("target_universe") == review_package.get("corporate_action_plan_universe") == VALIDATION_TARGET_UNIVERSE),
        _check("identity_authority_frozen_true", True, review_package.get("identity_authority_frozen")),
        _check("registry_inventory_approved_true", True, review_package.get("post_identity_freeze_registry_inventory_approved")),
        _check("corporate_action_plan_approved_true", True, review_package.get("corporate_action_authority_plan_approved")),
        _check("ready_for_split_event_authority_candidate_true", True, review_package.get("ready_for_split_event_authority_candidate")),
        _check("split_event_candidate_objective_reviewed", candidate_service.SPLIT_EVENT_AUTHORITY_CANDIDATE_OBJECTIVE, review_package.get("split_event_authority_candidate_objective")),
        _check("split_event_candidate_scope_candidate_only", candidate_service.SPLIT_EVENT_AUTHORITY_CANDIDATE_SCOPE, review_package.get("split_event_authority_candidate_scope")),
        _check("split_event_authority_creation_status_not_created", candidate_service.SPLIT_EVENT_AUTHORITY_CREATION_STATUS, review_package.get("split_event_authority_creation_status")),
        _check("split_event_authority_freeze_status_not_frozen", candidate_service.SPLIT_EVENT_AUTHORITY_FREEZE_STATUS, review_package.get("split_event_authority_freeze_status")),
        _check("per_ticker_split_event_candidate_entries_12", 12, len(entries)),
        _check("per_ticker_split_event_review_entries_12", 12, len(review_entries)),
        _check("per_ticker_split_event_candidate_status_ready", True, _all_entry_field(review_entries, "split_event_candidate_status", candidate_service.SPLIT_EVENT_CANDIDATE_READY_FOR_OPERATOR_REVIEW)),
        _check("per_ticker_split_event_review_status_ready", True, _all_entry_field(review_entries, "split_event_review_status", READY_FOR_OPERATOR_ASSESSMENT)),
        _check("per_ticker_split_event_authority_not_created", True, _all_entry_field(review_entries, "split_event_authority_status", candidate_service.NOT_CREATED)),
        _check("per_ticker_split_event_freeze_not_frozen", True, _all_entry_field(review_entries, "split_event_freeze_status", candidate_service.NOT_FROZEN)),
        _check("per_ticker_provider_evidence_request_not_authorized", True, _all_entry_field(review_entries, "provider_evidence_request_status", candidate_service.NOT_AUTHORIZED)),
        _check("per_ticker_provider_evidence_execution_not_executed", True, _all_entry_field(review_entries, "provider_evidence_execution_status", candidate_service.NOT_EXECUTED)),
        _check("per_ticker_split_history_not_fetched", True, _all_entry_field(review_entries, "split_history_status", candidate_service.NOT_FETCHED)),
        _check("per_ticker_split_event_candidate_digests_present", True, _digests_present(review_entries, "per_ticker_split_event_candidate_digest")),
        _check("per_ticker_split_event_review_digests_present", True, _digests_present(review_entries, "per_ticker_split_event_review_digest")),
        _check("split_event_evidence_requirements_reviewed", SPLIT_EVENT_EVIDENCE_REQUIREMENTS, review_package.get("split_event_evidence_requirements")),
        _check("split_event_evidence_requirement_policy_reviewed", SPLIT_EVENT_EVIDENCE_REQUIREMENT_POLICY, review_package.get("split_event_evidence_requirement_policy")),
        _check("future_split_provider_request_policy_reviewed", FUTURE_SPLIT_PROVIDER_REQUEST_POLICY, review_package.get("future_split_provider_request_policy")),
        _check("future_split_authority_chain_reviewed", FUTURE_SPLIT_AUTHORITY_CHAIN, review_package.get("future_split_authority_chain")),
        _check("future_corporate_action_readiness_chain_reviewed", FUTURE_CORPORATE_ACTION_READINESS_CHAIN, review_package.get("future_corporate_action_readiness_chain")),
        _check("future_gates_defined", FUTURE_GATES, review_package.get("future_gates")),
        _check("risk_controls_defined", RISK_CONTROLS, review_package.get("risk_controls")),
        _check("planned_outputs_8", 8, review_package.get("planned_output_count")),
        _check("planned_outputs_not_generated", True, _planned_outputs_not_generated(review_package)),
        _check("planned_outputs_research_only", True, _planned_outputs_research_only(review_package)),
        _check("provider_requests_made_in_review_false", False, review_package.get("provider_requests_made_in_review")),
        _check("live_validation_rerun_performed_false", False, review_package.get("live_validation_rerun_performed")),
        _check("live_provider_transport_enabled_in_review_false", False, review_package.get("live_provider_transport_enabled_in_review")),
        _check("split_event_authority_candidate_created_false", False, review_package.get("split_event_authority_candidate_created")),
        _check("split_event_authority_review_created_true", True, review_package.get("split_event_authority_review_created")),
        _check("split_event_authority_created_false", False, review_package.get("split_event_authority_created")),
        _check("split_event_authority_frozen_false", False, review_package.get("split_event_authority_frozen")),
        _check("split_provider_evidence_request_authorized_false", False, review_package.get("split_provider_evidence_request_authorized")),
        _check("split_provider_evidence_executed_false", False, review_package.get("split_provider_evidence_executed")),
        _check("split_provider_evidence_results_created_false", False, review_package.get("split_provider_evidence_results_created")),
        _check("dividend_event_authority_candidate_created_false", False, review_package.get("dividend_event_authority_candidate_created")),
        _check("dividend_event_authority_created_false", False, review_package.get("dividend_event_authority_created")),
        _check("dividend_event_authority_frozen_false", False, review_package.get("dividend_event_authority_frozen")),
        _check("corporate_action_authority_created_false", False, review_package.get("corporate_action_authority_created")),
        _check("new_ticker_acquisition_authorized_false", False, review_package.get("new_ticker_acquisition_authorized")),
        _check("dataset_generation_authorized_false", False, review_package.get("dataset_generation_authorized")),
        _check("acquisition_generation_authorized_false", False, review_package.get("acquisition_generation_authorized")),
        _check("canonical_dataset_authorized_false", False, review_package.get("canonical_dataset_authorized")),
        _check("registry_approval_created_false", False, review_package.get("registry_approval_created")),
        _check("additional_predictive_evidence_execution_authorized_false", False, review_package.get("additional_predictive_evidence_execution_authorized")),
        _check("additional_predictive_evidence_executed_false", False, review_package.get("additional_predictive_evidence_executed")),
        _check("predictive_experiment_rerun_authorized_false", False, review_package.get("predictive_experiment_rerun_authorized")),
        _check("predictive_experiment_rerun_performed_false", False, review_package.get("predictive_experiment_rerun_performed")),
        _check("walk_forward_rerun_performed_false", False, review_package.get("walk_forward_rerun_performed")),
        _check("label_regeneration_performed_false", False, review_package.get("label_regeneration_performed")),
        _check("feature_matrix_regeneration_performed_false", False, review_package.get("feature_matrix_regeneration_performed")),
        _check("new_strategy_scoring_performed_false", False, review_package.get("new_strategy_scoring_performed")),
        _check("trade_recommendations_generated_false", False, review_package.get("trade_recommendations_generated")),
        _check("predictive_usefulness_not_accepted", acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED, review_package.get("predictive_usefulness")),
        _check("predictive_usefulness_acceptance_ready_false", False, review_package.get("predictive_usefulness_acceptance_ready")),
        _check("predictive_usefulness_acceptance_recommended_false", False, review_package.get("predictive_usefulness_acceptance_recommended")),
        _check("predictive_usefulness_acceptance_candidate_created_false", False, review_package.get("predictive_usefulness_acceptance_candidate_created")),
        _check("profitability_not_accepted", acquisition.PROFITABILITY_NOT_ACCEPTED, review_package.get("profitability")),
        _check("profitability_acceptance_ready_false", False, review_package.get("profitability_acceptance_ready")),
        _check("profitability_acceptance_recommended_false", False, review_package.get("profitability_acceptance_recommended")),
        _check("runtime_migration_recommended_false", False, review_package.get("runtime_migration_recommended")),
        _check("runtime_migration_approved_false", False, review_package.get("runtime_migration_approved")),
        _check("runtime_migration_active_false", False, review_package.get("runtime_migration_active")),
        _check("strategy_runtime_migration_false", False, review_package.get("strategy_runtime_migration")),
        _check("runtime_use_not_authorized", _not_authorized(), review_package.get("runtime_use")),
        _check("strategy_use_not_authorized", _not_authorized(), review_package.get("strategy_use")),
        _check("paper_trading_not_authorized", _not_authorized(), review_package.get("paper_trading")),
        _check("broker_execution_not_authorized", _not_authorized(), review_package.get("broker_execution")),
        _check("automatic_stitching_false", False, review_package.get("automatic_stitching")),
        _check("no_split_event_authority_artifact_created", False, review_package.get("split_event_authority_artifact_created")),
        _check("no_split_event_authority_freeze_created", False, review_package.get("split_event_authority_freeze_created")),
        _check("no_split_provider_evidence_request_approval_created", False, review_package.get("split_provider_evidence_request_approval_created")),
        _check("no_split_provider_evidence_execution_created", False, review_package.get("split_provider_evidence_execution_created")),
        _check("no_dividend_event_authority_artifact_created", False, review_package.get("dividend_event_authority_artifact_created")),
        _check("no_corporate_action_authority_artifact_created", False, review_package.get("corporate_action_authority_artifact_created")),
        _check("no_acquisition_authorization_created", False, review_package.get("acquisition_authorization_created")),
        _check("no_dataset_generation_authorization_created", False, review_package.get("dataset_generation_authorization_created")),
        _check("no_predictive_usefulness_acceptance_artifact_created", False, review_package.get("predictive_usefulness_acceptance_artifact_created")),
        _check("no_profitability_acceptance_created", False, review_package.get("profitability_acceptance_created")),
        _check("no_runtime_migration_approval_created", False, review_package.get("runtime_migration_approval_created")),
    ]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [item for item in checklist if item["status"] != PASS]
    blockers = [item for item in failed if item["severity"] == BLOCKER]
    return {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": len(blockers),
        "ready_for_operator_assessment": not failed,
        "ready_for_split_provider_evidence_request_approval": False,
        "ready_for_split_event_authority_freeze": False,
        "split_event_authority_authorized": False,
        "split_event_authority_frozen": False,
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


def _review_package_digest_payload(review_package: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(review_package)
    payload.pop("split_event_authority_candidate_review_package_digest", None)
    return payload


def split_event_authority_candidate_review_package_digest_v1(
    review_package: dict[str, Any],
) -> str:
    """Return the deterministic semantic digest for the review package."""
    return semantic_digest(_review_package_digest_payload(review_package))


def build_split_event_authority_candidate_review_package_v1(
    candidate: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build the offline split-event authority candidate review package."""
    bound_candidate, binding_mode = _candidate_for_binding(candidate)
    review_package = _base_review_package(bound_candidate, binding_mode)
    checklist = _checklist(review_package)
    review_package["review_checklist"] = checklist
    review_package["review_summary"] = _summary(checklist)
    review_package["split_event_authority_candidate_review_package_digest"] = (
        split_event_authority_candidate_review_package_digest_v1(review_package)
    )
    validate_split_event_authority_candidate_review_package_v1(review_package)
    return review_package


def _reject_forbidden_values(
    mapping: dict[str, Any], *, path: str = "review_package"
) -> None:
    forbidden_strings = {
        "SPLIT_EVENT_AUTHORITY_APPROVED",
        "SPLIT_EVENT_AUTHORITY_FROZEN",
        "SPLIT_EVENT_PROVIDER_EVIDENCE_REQUEST_APPROVED",
        "SPLIT_EVENT_PROVIDER_EVIDENCE_EXECUTED",
        "DIVIDEND_EVENT_AUTHORITY_CANDIDATE",
        "DIVIDEND_EVENT_AUTHORITY_APPROVED",
        "DIVIDEND_EVENT_AUTHORITY_FROZEN",
        "CORPORATE_ACTION_AUTHORITY_APPROVED",
        "NEW_TICKER_ACQUISITION_AUTHORIZED",
        "ACQUISITION_GENERATION_AUTHORIZED",
        "CANONICAL_DATASET_AUTHORIZED",
        "REGISTRY_APPROVAL_CREATED",
        "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED",
        "PREDICTIVE_USEFULNESS_ACCEPTED",
        "PROFITABILITY_ACCEPTED",
        "RUNTIME_MIGRATION_APPROVED",
        "RUNTIME_MIGRATION_ACTIVE",
        "STRATEGY_RUNTIME_MIGRATION",
        "TRADE_RECOMMENDATIONS",
    }
    forbidden_true_fields = {
        "provider_requests_made_in_review",
        "live_validation_rerun_performed",
        "live_provider_transport_enabled_in_review",
        "split_event_authority_candidate_created",
        "split_event_authority_created",
        "split_event_authority_frozen",
        "split_event_authority_artifact_created",
        "split_event_authority_freeze_created",
        "split_provider_evidence_request_authorized",
        "split_provider_evidence_executed",
        "split_provider_evidence_results_created",
        "split_provider_evidence_request_approval_created",
        "split_provider_evidence_execution_created",
        "dividend_event_authority_candidate_created",
        "dividend_event_authority_review_created",
        "dividend_event_authority_created",
        "dividend_event_authority_frozen",
        "dividend_event_authority_artifact_created",
        "dividend_provider_evidence_request_authorized",
        "dividend_provider_evidence_executed",
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
    }
    for key, value in mapping.items():
        current_path = f"{path}.{key}"
        if isinstance(value, str) and value in forbidden_strings:
            raise SplitEventAuthorityCandidateReviewPackageError(
                f"{current_path} must not emit {value}"
            )
        if key in forbidden_true_fields and value is True:
            raise SplitEventAuthorityCandidateReviewPackageError(
                f"{current_path} must be false"
            )
        if isinstance(value, dict):
            _reject_forbidden_values(value, path=current_path)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, dict):
                    _reject_forbidden_values(item, path=f"{current_path}[{index}]")


def _validate_review_entries(review_package: dict[str, Any]) -> None:
    candidate_entries = _entries(review_package)
    review_entries = _review_entries_from_package(review_package)
    if len(candidate_entries) != 12:
        raise SplitEventAuthorityCandidateReviewPackageError(
            "per_ticker_split_event_candidate_entries mismatch"
        )
    if len(review_entries) != 12:
        raise SplitEventAuthorityCandidateReviewPackageError(
            "per_ticker_split_event_review_entries mismatch"
        )
    _expect(
        [entry.get("ticker") for entry in candidate_entries],
        VALIDATION_TARGET_UNIVERSE,
        "per_ticker_split_event_candidate_entries tickers",
    )
    _expect(
        [entry.get("ticker") for entry in review_entries],
        VALIDATION_TARGET_UNIVERSE,
        "per_ticker_split_event_review_entries tickers",
    )
    for entry in review_entries:
        ticker = entry.get("ticker")
        for field, expected in {
            "identity_authority_status": candidate_service.approval.review.plan.approval_service.review_service.candidate_service.freeze_service.IDENTITY_FREEZE_STATUS_FROZEN,
            "registry_inventory_status": candidate_service.approval.review.plan.approval_service.APPROVED_FOR_FUTURE_CORPORATE_ACTION_PLANNING_ONLY,
            "corporate_action_plan_status": candidate_service.approval.APPROVED_FOR_FUTURE_SPLIT_AND_DIVIDEND_AUTHORITY_CANDIDATES_ONLY,
            "split_event_candidate_status": candidate_service.SPLIT_EVENT_CANDIDATE_READY_FOR_OPERATOR_REVIEW,
            "split_event_review_status": READY_FOR_OPERATOR_ASSESSMENT,
            "split_event_authority_status": candidate_service.NOT_CREATED,
            "split_event_freeze_status": candidate_service.NOT_FROZEN,
            "provider_evidence_request_status": candidate_service.NOT_AUTHORIZED,
            "provider_evidence_execution_status": candidate_service.NOT_EXECUTED,
            "split_history_status": candidate_service.NOT_FETCHED,
            "split_event_count_status": candidate_service.NOT_EVALUATED,
            "acquisition_precondition_status": candidate_service.BLOCKED_UNTIL_SPLIT_AND_DIVIDEND_AUTHORITY_FROZEN_OR_EXPLICIT_POLICY,
            "runtime_use": _not_authorized(),
            "strategy_use": _not_authorized(),
            "paper_trading": _not_authorized(),
            "broker_execution": _not_authorized(),
        }.items():
            _expect(entry.get(field), expected, f"{ticker}.{field}")
        _expect_false(
            entry.get("corporate_action_authority_created"),
            f"{ticker}.corporate_action_authority_created",
        )
        _expect_false(
            entry.get("dataset_generation_authorized"),
            f"{ticker}.dataset_generation_authorized",
        )
        for field in (
            "source_identity_freeze_digest",
            "source_registry_inventory_approval_digest",
            "source_corporate_action_plan_approval_digest",
            "per_ticker_split_event_candidate_digest",
            "per_ticker_split_event_review_digest",
        ):
            digest = entry.get(field)
            if not isinstance(digest, str) or len(digest) != 64:
                raise SplitEventAuthorityCandidateReviewPackageError(
                    f"{field} missing"
                )
        _expect(
            entry["per_ticker_split_event_candidate_digest"],
            candidate_service.per_ticker_split_event_candidate_digest_v1(
                _candidate_entry_from_review_entry(entry)
            ),
            f"{ticker}.per_ticker_split_event_candidate_digest",
        )
        _expect(
            entry["per_ticker_split_event_review_digest"],
            per_ticker_split_event_review_digest_v1(entry),
            f"{ticker}.per_ticker_split_event_review_digest",
        )


def validate_split_event_authority_candidate_review_package_v1(
    review_package: dict[str, Any],
) -> dict[str, Any]:
    """Validate the split-event authority candidate review package."""
    if not isinstance(review_package, dict):
        raise SplitEventAuthorityCandidateReviewPackageError(
            "review_package must be a JSON object"
        )
    _reject_forbidden_values(review_package)
    _expect(
        review_package.get("artifact_kind"),
        ARTIFACT_KIND_SPLIT_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE,
        "artifact_kind",
    )
    _expect(
        review_package.get("schema_version"),
        SCHEMA_VERSION_SPLIT_EVENT_AUTHORITY_CANDIDATE_REVIEW_V1,
        "schema_version",
    )
    _expect(
        review_package.get("review_status"),
        SPLIT_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_READY,
        "review_status",
    )
    if review_package.get("split_event_authority_candidate_binding_mode") not in {
        SPLIT_EVENT_AUTHORITY_CANDIDATE_STATUS_BINDING,
        SPLIT_EVENT_AUTHORITY_CANDIDATE_OBJECT_BINDING,
    }:
        raise SplitEventAuthorityCandidateReviewPackageError(
            "split_event_authority_candidate_binding_mode mismatch"
        )
    for field in (
        "created_offline",
        "split_event_authority_review_created",
        "corporate_action_authority_plan_approved",
        "ready_for_split_event_authority_candidate",
        "ready_for_dividend_event_authority_candidate",
        "post_identity_freeze_registry_inventory_approved",
        "identity_authority_created",
        "identity_authority_frozen",
        "new_ticker_identity_authority_created",
        "research_only",
        "operator_review_required",
    ):
        _expect_true(review_package.get(field), field)
    for field in (
        "provider_requests_made_in_review",
        "live_validation_rerun_performed",
        "live_provider_transport_enabled_in_review",
        "split_event_authority_candidate_created",
        "split_event_authority_created",
        "split_event_authority_frozen",
        "split_event_authority_artifact_created",
        "split_event_authority_freeze_created",
        "split_provider_evidence_request_authorized",
        "split_provider_evidence_executed",
        "split_provider_evidence_results_created",
        "split_provider_evidence_request_approval_created",
        "split_provider_evidence_execution_created",
        "corporate_action_authority_created",
        "corporate_action_authority_artifact_created",
        "ready_for_split_event_provider_evidence_request_approval",
        "ready_for_split_event_authority_freeze",
        "dividend_event_authority_candidate_created",
        "dividend_event_authority_review_created",
        "dividend_event_authority_created",
        "dividend_event_authority_frozen",
        "dividend_event_authority_artifact_created",
        "dividend_provider_evidence_request_authorized",
        "dividend_provider_evidence_executed",
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
        _expect_false(review_package.get(field), field)
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(review_package.get(field), _not_authorized(), field)
    for field, expected in {
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "reviewed_split_event_authority_candidate_kind": candidate_service.ARTIFACT_KIND_SPLIT_EVENT_AUTHORITY_CANDIDATE,
        "reviewed_split_event_authority_candidate_status": candidate_service.SPLIT_EVENT_AUTHORITY_READY_FOR_OPERATOR_REVIEW,
        "reviewed_split_event_authority_candidate_digest": EXPECTED_REVIEWED_SPLIT_EVENT_AUTHORITY_CANDIDATE_DIGEST,
        "reviewed_split_event_authority_candidate_checklist_total": EXPECTED_REVIEWED_SPLIT_EVENT_AUTHORITY_CANDIDATE_CHECKLIST_TOTAL,
        "reviewed_split_event_authority_candidate_checklist_passed": EXPECTED_REVIEWED_SPLIT_EVENT_AUTHORITY_CANDIDATE_CHECKLIST_PASSED,
        "reviewed_split_event_authority_candidate_checklist_failed": EXPECTED_REVIEWED_SPLIT_EVENT_AUTHORITY_CANDIDATE_CHECKLIST_FAILED,
        "reviewed_split_event_authority_candidate_blocker_count": EXPECTED_REVIEWED_SPLIT_EVENT_AUTHORITY_CANDIDATE_BLOCKER_COUNT,
        "split_event_authority_candidate_digest": EXPECTED_REVIEWED_SPLIT_EVENT_AUTHORITY_CANDIDATE_DIGEST,
        "source_corporate_action_plan_approval_kind": candidate_service.approval.ARTIFACT_KIND_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVED,
        "source_corporate_action_plan_approval_status": candidate_service.approval.CORPORATE_ACTION_AUTHORITY_PLAN_APPROVED,
        "source_corporate_action_plan_approval_scope": candidate_service.approval.CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_ONLY,
        "corporate_action_authority_plan_approval_digest": candidate_service.EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST,
        "corporate_action_authority_plan_candidate_review_package_digest": candidate_service.EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "corporate_action_authority_plan_candidate_digest": candidate_service.EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_DIGEST,
        "post_identity_freeze_registry_inventory_approval_digest": candidate_service.approval.review.plan.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST,
        "post_identity_freeze_registry_inventory_candidate_review_package_digest": candidate_service.approval.review.plan.approval_service.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "post_identity_freeze_registry_inventory_candidate_digest": candidate_service.approval.review.plan.approval_service.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_DIGEST,
        "identity_authority_freeze_digest": candidate_service.approval.review.plan.approval_service.review_service.candidate_service.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
        "identity_authority_candidate_review_package_digest": candidate_service.approval.review.plan.approval_service.review_service.candidate_service.freeze_service.EXPECTED_IDENTITY_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "identity_authority_candidate_digest": candidate_service.approval.review.plan.approval_service.review_service.candidate_service.freeze_service.EXPECTED_IDENTITY_AUTHORITY_CANDIDATE_DIGEST,
        "live_ticker_validation_results_review_package_digest": candidate_service.approval.review.plan.approval_service.review_service.candidate_service.freeze_service.EXPECTED_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_DIGEST,
        "live_ticker_validation_execution_digest": candidate_service.approval.review.plan.approval_service.review_service.candidate_service.freeze_service.EXPECTED_LIVE_TICKER_VALIDATION_EXECUTION_DIGEST,
        "ticker_universe_selection_approval_digest": candidate_service.approval.review.plan.approval_service.review_service.candidate_service.freeze_service.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST,
        "target_universe": VALIDATION_TARGET_UNIVERSE,
        "corporate_action_plan_universe": VALIDATION_TARGET_UNIVERSE,
        "target_universe_count": 12,
        "authority_scope": candidate_service.approval.review.plan.approval_service.review_service.candidate_service.freeze_service.IDENTITY_AUTHORITY_ONLY,
        "split_event_authority_candidate_objective": candidate_service.SPLIT_EVENT_AUTHORITY_CANDIDATE_OBJECTIVE,
        "split_event_authority_candidate_scope": candidate_service.SPLIT_EVENT_AUTHORITY_CANDIDATE_SCOPE,
        "split_event_authority_creation_status": candidate_service.SPLIT_EVENT_AUTHORITY_CREATION_STATUS,
        "split_event_authority_freeze_status": candidate_service.SPLIT_EVENT_AUTHORITY_FREEZE_STATUS,
        "split_event_evidence_requirements": SPLIT_EVENT_EVIDENCE_REQUIREMENTS,
        "split_event_evidence_requirement_policy": SPLIT_EVENT_EVIDENCE_REQUIREMENT_POLICY,
        "future_split_provider_request_policy": FUTURE_SPLIT_PROVIDER_REQUEST_POLICY,
        "future_split_authority_chain": FUTURE_SPLIT_AUTHORITY_CHAIN,
        "future_corporate_action_readiness_chain": FUTURE_CORPORATE_ACTION_READINESS_CHAIN,
        "future_gates": FUTURE_GATES,
        "risk_controls": RISK_CONTROLS,
        "planned_output_count": 8,
        "planned_outputs_status": candidate_service.PLANNED_NOT_GENERATED,
        "planned_outputs_label": candidate_service.RESEARCH_ONLY_NON_ACTIONABLE,
    }.items():
        if field in {
            "split_event_evidence_requirements",
            "future_split_provider_request_policy",
            "future_split_authority_chain",
            "future_corporate_action_readiness_chain",
            "future_gates",
            "risk_controls",
        } and not review_package.get(field):
            raise SplitEventAuthorityCandidateReviewPackageError(f"{field} missing")
        _expect(review_package.get(field), expected, field)
    if review_package.get("target_universe") != review_package.get(
        "corporate_action_plan_universe"
    ):
        raise SplitEventAuthorityCandidateReviewPackageError(
            "target universe differs from split candidate universe"
        )
    if not _planned_outputs_not_generated(review_package):
        raise SplitEventAuthorityCandidateReviewPackageError(
            "planned_outputs must not be generated"
        )
    if not _planned_outputs_research_only(review_package):
        raise SplitEventAuthorityCandidateReviewPackageError(
            "planned_outputs must be research only"
        )
    _validate_review_entries(review_package)
    checklist = review_package.get("review_checklist")
    if not isinstance(checklist, list):
        raise SplitEventAuthorityCandidateReviewPackageError(
            "review_checklist missing"
        )
    _expect(
        [item.get("check_id") for item in checklist if isinstance(item, dict)],
        REQUIRED_CHECK_IDS,
        "review_checklist check IDs",
    )
    expected_checklist = _checklist(review_package)
    failed = [item for item in expected_checklist if item["status"] != PASS]
    if failed:
        raise SplitEventAuthorityCandidateReviewPackageError(
            f"review checklist contains failed check: {failed[0]['check_id']}"
        )
    _expect(checklist, expected_checklist, "review_checklist")
    expected_summary = _summary(expected_checklist)
    _expect(review_package.get("review_summary"), expected_summary, "review_summary")
    _expect_true(
        expected_summary.get("ready_for_operator_assessment"),
        "ready_for_operator_assessment",
    )
    digest = review_package.get("split_event_authority_candidate_review_package_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise SplitEventAuthorityCandidateReviewPackageError(
            "split_event_authority_candidate_review_package_digest missing"
        )
    _expect(
        digest,
        split_event_authority_candidate_review_package_digest_v1(review_package),
        "split_event_authority_candidate_review_package_digest",
    )
    return {
        "status": "SPLIT_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_VALID",
        "artifact_kind": review_package["artifact_kind"],
        "review_status": review_package["review_status"],
        "split_event_authority_candidate_review_package_digest": digest,
        "reviewed_split_event_authority_candidate_digest": review_package[
            "reviewed_split_event_authority_candidate_digest"
        ],
        "corporate_action_authority_plan_approval_digest": review_package[
            "corporate_action_authority_plan_approval_digest"
        ],
        "post_identity_freeze_registry_inventory_approval_digest": review_package[
            "post_identity_freeze_registry_inventory_approval_digest"
        ],
        "identity_authority_freeze_digest": review_package[
            "identity_authority_freeze_digest"
        ],
        "target_universe_count": review_package["target_universe_count"],
        "per_ticker_split_event_review_entry_count": len(
            _review_entries_from_package(review_package)
        ),
        "total_checks": review_package["review_summary"]["total_checks"],
        "passed_checks": review_package["review_summary"]["passed_checks"],
        "failed_checks": review_package["review_summary"]["failed_checks"],
        "blocker_count": review_package["review_summary"]["blocker_count"],
        "ready_for_operator_assessment": review_package["review_summary"][
            "ready_for_operator_assessment"
        ],
        "ready_for_split_provider_evidence_request_approval": False,
        "ready_for_split_event_authority_freeze": False,
        "split_event_authority_authorized": False,
        "split_event_authority_frozen": False,
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


def build_split_event_authority_candidate_review_markdown_v1(
    review_package: dict[str, Any],
) -> str:
    """Render a sanitized split-event authority candidate review status document."""
    validation = validate_split_event_authority_candidate_review_package_v1(
        review_package
    )
    summary = review_package["review_summary"]
    lines = [
        "# MarketFlow Split Event Authority Candidate Operator Review Package Status",
        "",
        "## Title",
        "- Split Event Authority Candidate Operator Review Package v1.",
        "",
        "## Reviewed Split Event Authority Candidate",
        f"- Candidate kind: `{review_package['reviewed_split_event_authority_candidate_kind']}`",
        f"- Candidate status: `{review_package['reviewed_split_event_authority_candidate_status']}`",
        f"- Candidate digest: `{review_package['reviewed_split_event_authority_candidate_digest']}`",
        f"- Review package digest: `{validation['split_event_authority_candidate_review_package_digest']}`",
        "",
        "## Source Corporate-Action Plan Approval",
        f"- Approval digest: `{review_package['corporate_action_authority_plan_approval_digest']}`",
        f"- Plan review package digest: `{review_package['corporate_action_authority_plan_candidate_review_package_digest']}`",
        f"- Plan candidate digest: `{review_package['corporate_action_authority_plan_candidate_digest']}`",
        "",
        "## Bound Source Digests",
        f"- Registry inventory approval digest: `{review_package['post_identity_freeze_registry_inventory_approval_digest']}`",
        f"- Registry inventory review package digest: `{review_package['post_identity_freeze_registry_inventory_candidate_review_package_digest']}`",
        f"- Registry inventory candidate digest: `{review_package['post_identity_freeze_registry_inventory_candidate_digest']}`",
        f"- Identity authority freeze digest: `{review_package['identity_authority_freeze_digest']}`",
        f"- Identity authority candidate review package digest: `{review_package['identity_authority_candidate_review_package_digest']}`",
        f"- Identity authority candidate digest: `{review_package['identity_authority_candidate_digest']}`",
        f"- Live ticker validation results review package digest: `{review_package['live_ticker_validation_results_review_package_digest']}`",
        f"- Live ticker validation execution digest: `{review_package['live_ticker_validation_execution_digest']}`",
        f"- Ticker universe selection approval digest: `{review_package['ticker_universe_selection_approval_digest']}`",
        "",
        "## Target Universe",
        f"- Target universe count: `{review_package['target_universe_count']}`",
        "- Target universe: " + ", ".join(f"`{ticker}`" for ticker in review_package["target_universe"]),
        "",
        "## Split Event Authority Candidate Objective",
        f"- split_event_authority_candidate_objective: `{review_package['split_event_authority_candidate_objective']}`",
        f"- split_event_authority_candidate_scope: `{review_package['split_event_authority_candidate_scope']}`",
        f"- split_event_authority_creation_status: `{review_package['split_event_authority_creation_status']}`",
        f"- split_event_authority_freeze_status: `{review_package['split_event_authority_freeze_status']}`",
        "",
        "## Per-Ticker Split Event Review",
    ]
    lines.extend(
        f"- `{entry['ticker']}`: `{entry['split_event_review_status']}`, candidate digest `{entry['per_ticker_split_event_candidate_digest']}`, review digest `{entry['per_ticker_split_event_review_digest']}`"
        for entry in review_package["per_ticker_split_event_review_entries"]
    )
    lines.extend(["", "## Split Event Evidence Requirements"])
    lines.extend(f"- `{item}`" for item in review_package["split_event_evidence_requirements"])
    lines.extend(["", "## Future Split Provider Request Policy"])
    lines.extend(
        f"- `{key}`: `{value}`"
        for key, value in review_package["future_split_provider_request_policy"].items()
    )
    lines.extend(["", "## Future Split Authority Chain"])
    lines.extend(
        f"{index}. {step}"
        for index, step in enumerate(
            review_package["future_split_authority_chain"], start=1
        )
    )
    lines.extend(["", "## Future Corporate-Action Readiness Chain"])
    lines.extend(
        f"{index}. {step}"
        for index, step in enumerate(
            review_package["future_corporate_action_readiness_chain"], start=1
        )
    )
    lines.extend(["", "## Future Gates"])
    lines.extend(f"- `{item}`" for item in review_package["future_gates"])
    lines.extend(["", "## Risk Controls"])
    lines.extend(f"- `{item}`" for item in review_package["risk_controls"])
    lines.extend(
        [
            "",
            "## Split Authority Boundary",
            f"- split_event_authority_candidate_created: `{review_package['split_event_authority_candidate_created']}`",
            f"- split_event_authority_review_created: `{review_package['split_event_authority_review_created']}`",
            f"- split_event_authority_created: `{review_package['split_event_authority_created']}`",
            f"- split_event_authority_frozen: `{review_package['split_event_authority_frozen']}`",
            f"- split_provider_evidence_request_authorized: `{review_package['split_provider_evidence_request_authorized']}`",
            f"- split_provider_evidence_executed: `{review_package['split_provider_evidence_executed']}`",
            f"- split_provider_evidence_results_created: `{review_package['split_provider_evidence_results_created']}`",
            "",
            "## Dividend Boundary",
            f"- dividend_event_authority_candidate_created: `{review_package['dividend_event_authority_candidate_created']}`",
            f"- dividend_event_authority_created: `{review_package['dividend_event_authority_created']}`",
            f"- dividend_event_authority_frozen: `{review_package['dividend_event_authority_frozen']}`",
            "",
            "## Corporate-Action Authority Boundary",
            f"- corporate_action_authority_plan_approved: `{review_package['corporate_action_authority_plan_approved']}`",
            f"- corporate_action_authority_created: `{review_package['corporate_action_authority_created']}`",
            f"- corporate_action_authority_artifact_created: `{review_package['corporate_action_authority_artifact_created']}`",
            "",
            "## Acquisition Boundary",
            f"- new_ticker_acquisition_authorized: `{review_package['new_ticker_acquisition_authorized']}`",
            f"- acquisition_generation_authorized: `{review_package['acquisition_generation_authorized']}`",
            f"- acquisition_authorization_created: `{review_package['acquisition_authorization_created']}`",
            "",
            "## Dataset Boundary",
            f"- dataset_generation_authorized: `{review_package['dataset_generation_authorized']}`",
            f"- dataset_generation_authorization_created: `{review_package['dataset_generation_authorization_created']}`",
            f"- canonical_dataset_authorized: `{review_package['canonical_dataset_authorized']}`",
            f"- registry_approval_created: `{review_package['registry_approval_created']}`",
            "",
            "## Predictive/Profitability Boundary",
            f"- additional_predictive_evidence_execution_authorized: `{review_package['additional_predictive_evidence_execution_authorized']}`",
            f"- additional_predictive_evidence_executed: `{review_package['additional_predictive_evidence_executed']}`",
            f"- predictive_usefulness: `{review_package['predictive_usefulness']}`",
            f"- profitability: `{review_package['profitability']}`",
            "",
            "## Runtime Boundary",
            f"- runtime_migration_approved: `{review_package['runtime_migration_approved']}`",
            f"- runtime_migration_active: `{review_package['runtime_migration_active']}`",
            f"- runtime_use: `{review_package['runtime_use']}`",
            f"- strategy_use: `{review_package['strategy_use']}`",
            f"- paper_trading: `{review_package['paper_trading']}`",
            f"- broker_execution: `{review_package['broker_execution']}`",
            "",
            "## Checklist Summary",
            f"- Total checks: `{summary['total_checks']}`",
            f"- Passed checks: `{summary['passed_checks']}`",
            f"- Failed checks: `{summary['failed_checks']}`",
            f"- Blocker count: `{summary['blocker_count']}`",
            f"- Ready for operator assessment: `{summary['ready_for_operator_assessment']}`",
            f"- Ready for split provider evidence request approval: `{summary['ready_for_split_provider_evidence_request_approval']}`",
            f"- Ready for split event authority freeze: `{summary['ready_for_split_event_authority_freeze']}`",
            "",
            "## Guardrails",
            "- Created offline: `True`",
            "- No Massive.com / Polygon provider split evidence was fetched.",
            "- No provider evidence request approval, provider evidence execution, split authority, or split freeze was created.",
            "- Dividend authority, corporate-action authority, acquisition, and dataset generation remain unauthorized.",
            "- Runtime, strategy, paper trading, and broker execution use remain `NOT_AUTHORIZED`.",
            "",
        ]
    )
    return "\n".join(lines)


def write_split_event_authority_candidate_review_package_v1(
    output_dir: str | Path,
    *,
    candidate: dict[str, Any] | None = None,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write the review package JSON without overwriting an existing artifact."""
    review_package = build_split_event_authority_candidate_review_package_v1(
        candidate=candidate
    )
    validation = validate_split_event_authority_candidate_review_package_v1(
        review_package
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "split_event_authority_candidate_review_package_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise SplitEventAuthorityCandidateReviewPackageError(
            "split event authority candidate review filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise SplitEventAuthorityCandidateReviewPackageError(
            "split event authority candidate review output already exists"
        )
    payload = canonical_json_bytes(review_package)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": _path_text(path),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
    }
