"""Offline operator review package for the expanded-universe identity authority candidate."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import expanded_universe_per_ticker_identity_authority_candidate_service as candidate_service


ARTIFACT_KIND_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_CANDIDATE_REVIEW_PACKAGE = (
    "EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_CANDIDATE_REVIEW_PACKAGE"
)
SCHEMA_VERSION_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_CANDIDATE_REVIEW_V1 = (
    "expanded_universe_per_ticker_identity_authority_candidate_review_v1"
)
EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_READY = (
    "EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_READY"
)
EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_CANDIDATE_STATUS_BINDING = (
    "EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_CANDIDATE_STATUS_BINDING"
)
EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_CANDIDATE_OBJECT_BINDING = (
    "EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_CANDIDATE_OBJECT_BINDING"
)

EXPECTED_IDENTITY_AUTHORITY_CANDIDATE_DIGEST = (
    "0cb27ba65d1dfc57c73f716fdae9bc6baf803770ec11a8ea5868728f58711d3c"
)
EXPECTED_REVIEWED_IDENTITY_AUTHORITY_CANDIDATE_CHECKLIST_TOTAL = 75
EXPECTED_REVIEWED_IDENTITY_AUTHORITY_CANDIDATE_CHECKLIST_PASSED = 75
EXPECTED_REVIEWED_IDENTITY_AUTHORITY_CANDIDATE_CHECKLIST_FAILED = 0
EXPECTED_REVIEWED_IDENTITY_AUTHORITY_CANDIDATE_BLOCKER_COUNT = 0

REVIEW_ONLY_NOT_FREEZE = "REVIEW_ONLY_NOT_FREEZE"
CANDIDATE_REVIEW_ONLY_NOT_FROZEN = "CANDIDATE_REVIEW_ONLY_NOT_FROZEN"
REVIEW_PACKAGE_CREATED = "REVIEW_PACKAGE_CREATED"
READY_FOR_OPERATOR_ASSESSMENT = "READY_FOR_OPERATOR_ASSESSMENT"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

VALIDATION_TARGET_UNIVERSE = list(candidate_service.VALIDATION_TARGET_UNIVERSE)
IDENTITY_FIELDS_TO_BIND = list(candidate_service.IDENTITY_FIELDS_TO_BIND)
IDENTITY_FIELD_GROUPS = deepcopy(candidate_service.IDENTITY_FIELD_GROUPS)
IDENTITY_EVIDENCE_LIMITATIONS = list(candidate_service.IDENTITY_EVIDENCE_LIMITATIONS)
FUTURE_IDENTITY_AUTHORITY_CHAIN = [
    "Identity evidence discrepancy triage, if required.",
    "Per-ticker identity authority freeze ceremony.",
    "Post-freeze identity registry/read-only discovery.",
    "Corporate-action authority chain only after identity freeze.",
    "Acquisition generation chain only after identity and corporate-action authority.",
    "Canonical dataset chain only after acquisition freeze.",
    "Research registry approval only after canonical dataset freeze.",
]
FUTURE_GATES = [
    "identity_evidence_discrepancy_triage_if_needed",
    "per_ticker_identity_authority_freeze_approval",
    "identity_freeze_ceremony",
    "post_identity_freeze_registry_inventory",
    "corporate_action_authority_chain_candidate",
    "acquisition_generation_chain_candidate",
    "canonical_dataset_chain_candidate",
    "research_registry_chain_candidate",
]
RISK_CONTROLS = list(candidate_service.RISK_CONTROLS)

REQUIRED_CHECK_IDS = [
    "identity_authority_candidate_kind_matches",
    "identity_authority_candidate_status_ready_for_review",
    "identity_authority_candidate_digest_matches",
    "identity_authority_candidate_checklist_zero_blockers",
    "identity_plan_review_digest_bound",
    "identity_plan_candidate_digest_bound",
    "live_validation_results_review_digest_bound",
    "live_validation_execution_digest_bound",
    "live_validation_approval_digest_bound",
    "ticker_universe_selection_approval_digest_bound",
    "target_universe_count_12",
    "target_universe_matches_validated_universe",
    "all_targets_validated_read_only",
    "identity_review_scope_review_only_not_freeze",
    "per_ticker_identity_candidate_entries_12",
    "per_ticker_identity_review_entries_12",
    "per_ticker_identity_review_status_ready",
    "per_ticker_identity_authority_created_false",
    "per_ticker_identity_freeze_status_not_frozen",
    "identity_fields_to_bind_reviewed",
    "identity_fields_use_status_value_structure",
    "unavailable_fields_marked_unavailable_not_fabricated",
    "provider_response_digest_bound_or_marked_unavailable",
    "sanitized_validation_digest_bound_or_marked_unavailable",
    "per_ticker_identity_candidate_digests_present",
    "per_ticker_identity_review_digests_present",
    "identity_field_classification_reviewed",
    "identity_evidence_limitations_recorded",
    "future_identity_authority_chain_defined",
    "future_gates_defined",
    "risk_controls_defined",
    "provider_requests_made_in_review_false",
    "live_validation_rerun_performed_false",
    "live_provider_transport_enabled_in_review_false",
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
    "no_identity_authority_freeze_created",
    "no_corporate_action_authority_created",
    "no_acquisition_authorization_created",
    "no_dataset_generation_authorization_created",
    "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created",
    "no_runtime_migration_approval_created",
]


class ExpandedUniversePerTickerIdentityAuthorityCandidateReviewPackageError(ValueError):
    """Raised when the identity authority candidate review package is invalid."""


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
        raise ExpandedUniversePerTickerIdentityAuthorityCandidateReviewPackageError(
            f"{field_name} mismatch"
        )


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise ExpandedUniversePerTickerIdentityAuthorityCandidateReviewPackageError(
            f"{field_name} must be true"
        )


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise ExpandedUniversePerTickerIdentityAuthorityCandidateReviewPackageError(
            f"{field_name} must be false"
        )


def _path_text(path: Path) -> str:
    return str(path).replace("\\", "/")


def _candidate_for_binding(candidate: dict[str, Any] | None) -> tuple[dict[str, Any], str]:
    if candidate is None:
        return (
            candidate_service.build_expanded_universe_per_ticker_identity_authority_candidate_v1(),
            EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_CANDIDATE_STATUS_BINDING,
        )
    candidate_service.validate_expanded_universe_per_ticker_identity_authority_candidate_v1(
        candidate
    )
    return (
        deepcopy(candidate),
        EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_CANDIDATE_OBJECT_BINDING,
    )


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


def _identity_fields_have_value_status(entries: list[dict[str, Any]]) -> bool:
    return candidate_service._fields_have_value_status(entries)


def _unavailable_fields_not_fabricated(entries: list[dict[str, Any]]) -> bool:
    return candidate_service._unavailable_fields_not_fabricated(entries)


def _digest_field_bound_or_unavailable(entries: list[dict[str, Any]], field_name: str) -> bool:
    return candidate_service._digest_field_bound_or_unavailable(entries, field_name)


def _per_ticker_identity_review_digest_payload(entry: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(entry)
    payload.pop("per_ticker_identity_review_digest", None)
    return payload


def per_ticker_identity_review_digest_v1(entry: dict[str, Any]) -> str:
    """Return the deterministic semantic digest for one per-ticker identity review entry."""
    return semantic_digest(_per_ticker_identity_review_digest_payload(entry))


def _review_entries(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for source in candidate.get("per_ticker_identity_candidate_entries", []):
        entry = {
            "ticker": source.get("ticker"),
            "identity_candidate_status": source.get("identity_candidate_status"),
            "identity_review_status": REVIEW_PACKAGE_CREATED,
            "identity_authority_scope": CANDIDATE_REVIEW_ONLY_NOT_FROZEN,
            "identity_authority_created": False,
            "identity_freeze_status": candidate_service.plan_review.plan.NOT_FROZEN,
            "identity_fields": deepcopy(source.get("identity_fields")),
            "identity_evidence_limitations": list(IDENTITY_EVIDENCE_LIMITATIONS),
            "per_ticker_identity_candidate_digest": source.get(
                "per_ticker_identity_candidate_digest"
            ),
            "per_ticker_identity_review_status": READY_FOR_OPERATOR_ASSESSMENT,
        }
        entry["per_ticker_identity_review_digest"] = per_ticker_identity_review_digest_v1(
            entry
        )
        entries.append(entry)
    return entries


def _base_review_package(candidate: dict[str, Any], binding_mode: str) -> dict[str, Any]:
    summary = candidate["candidate_summary"]
    return {
        "artifact_kind": (
            ARTIFACT_KIND_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_CANDIDATE_REVIEW_PACKAGE
        ),
        "schema_version": SCHEMA_VERSION_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_CANDIDATE_REVIEW_V1,
        "review_status": (
            EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_READY
        ),
        "identity_authority_candidate_binding_mode": binding_mode,
        "operator_decision_required": True,
        "operator_decision": None,
        "created_offline": True,
        "provider_requests_made_in_review": False,
        "live_validation_rerun_performed": False,
        "live_provider_transport_enabled_in_review": False,
        "source_output_file_reinspection_performed": False,
        "identity_authority_candidate_review_scope": REVIEW_ONLY_NOT_FREEZE,
        "per_ticker_identity_authority_candidate_created": True,
        "per_ticker_identity_authority_review_created": True,
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
        "runtime_use": candidate_service.plan_review.plan.NOT_AUTHORIZED,
        "strategy_use": candidate_service.plan_review.plan.NOT_AUTHORIZED,
        "paper_trading": candidate_service.plan_review.plan.NOT_AUTHORIZED,
        "broker_execution": candidate_service.plan_review.plan.NOT_AUTHORIZED,
        "automatic_stitching": False,
        "reviewed_identity_authority_candidate_kind": candidate["artifact_kind"],
        "reviewed_identity_authority_candidate_status": candidate["candidate_status"],
        "reviewed_identity_authority_candidate_digest": candidate[
            "expanded_universe_per_ticker_identity_authority_candidate_digest"
        ],
        "reviewed_identity_authority_candidate_checklist_total": summary["total_checks"],
        "reviewed_identity_authority_candidate_checklist_passed": summary["passed_checks"],
        "reviewed_identity_authority_candidate_checklist_failed": summary["failed_checks"],
        "reviewed_identity_authority_candidate_blocker_count": summary["blocker_count"],
        "identity_authority_candidate_digest": candidate[
            "expanded_universe_per_ticker_identity_authority_candidate_digest"
        ],
        "identity_authority_plan_candidate_review_package_digest": candidate[
            "identity_authority_plan_candidate_review_package_digest"
        ],
        "identity_authority_plan_candidate_digest": candidate[
            "identity_authority_plan_candidate_digest"
        ],
        "live_ticker_validation_results_review_package_digest": candidate[
            "live_ticker_validation_results_review_package_digest"
        ],
        "live_ticker_validation_execution_digest": candidate[
            "live_ticker_validation_execution_digest"
        ],
        "live_ticker_validation_approval_digest": candidate[
            "live_ticker_validation_approval_digest"
        ],
        "live_ticker_validation_candidate_digest": candidate[
            "live_ticker_validation_candidate_digest"
        ],
        "live_ticker_validation_candidate_review_package_digest": candidate[
            "live_ticker_validation_candidate_review_package_digest"
        ],
        "ticker_universe_selection_approval_digest": candidate[
            "ticker_universe_selection_approval_digest"
        ],
        "ticker_universe_selection_candidate_digest": candidate[
            "ticker_universe_selection_candidate_digest"
        ],
        "ticker_universe_selection_candidate_review_package_digest": candidate[
            "ticker_universe_selection_candidate_review_package_digest"
        ],
        "target_universe": list(candidate["target_universe"]),
        "validated_universe": list(candidate["validated_universe"]),
        "target_universe_count": candidate["target_universe_count"],
        "all_targets_validated_read_only": candidate["all_targets_validated_read_only"],
        "validated_read_only_count": candidate["validated_read_only_count"],
        "provider_request_count": candidate["provider_request_count"],
        "successful_provider_response_count": candidate["successful_provider_response_count"],
        "failed_provider_response_count": candidate["failed_provider_response_count"],
        "identity_fields_to_bind": list(candidate["identity_fields_to_bind"]),
        "identity_field_groups": deepcopy(candidate["identity_field_groups"]),
        "identity_evidence_limitations": list(candidate["identity_evidence_limitations"]),
        "per_ticker_identity_candidate_entries": deepcopy(
            candidate["per_ticker_identity_candidate_entries"]
        ),
        "per_ticker_identity_review_entries": _review_entries(candidate),
        "future_identity_authority_chain": _future_identity_authority_chain(),
        "future_gates": list(FUTURE_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "identity_authority_freeze_created": False,
        "corporate_action_authority_authorized": False,
        "acquisition_authorized": False,
        "acquisition_authorization_created": False,
        "dataset_generation_authorization_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
    }


def _candidate_entries(review_package: dict[str, Any]) -> list[dict[str, Any]]:
    entries = review_package.get("per_ticker_identity_candidate_entries")
    return entries if isinstance(entries, list) else []


def _review_entries_from_package(review_package: dict[str, Any]) -> list[dict[str, Any]]:
    entries = review_package.get("per_ticker_identity_review_entries")
    return entries if isinstance(entries, list) else []


def _checklist(review_package: dict[str, Any]) -> list[dict[str, Any]]:
    candidate_entries = _candidate_entries(review_package)
    review_entries = _review_entries_from_package(review_package)
    expected_candidate_digest = (
        EXPECTED_IDENTITY_AUTHORITY_CANDIDATE_DIGEST
        if review_package.get("identity_authority_candidate_binding_mode")
        == EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_CANDIDATE_STATUS_BINDING
        else review_package.get("identity_authority_candidate_digest")
    )
    return [
        _check(
            "identity_authority_candidate_kind_matches",
            candidate_service.ARTIFACT_KIND_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_CANDIDATE,
            review_package.get("reviewed_identity_authority_candidate_kind"),
        ),
        _check(
            "identity_authority_candidate_status_ready_for_review",
            candidate_service.EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_READY_FOR_OPERATOR_REVIEW,
            review_package.get("reviewed_identity_authority_candidate_status"),
        ),
        _check(
            "identity_authority_candidate_digest_matches",
            expected_candidate_digest,
            review_package.get("reviewed_identity_authority_candidate_digest"),
        ),
        _check(
            "identity_authority_candidate_checklist_zero_blockers",
            0,
            review_package.get("reviewed_identity_authority_candidate_blocker_count"),
        ),
        _check(
            "identity_plan_review_digest_bound",
            candidate_service.EXPECTED_IDENTITY_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST,
            review_package.get("identity_authority_plan_candidate_review_package_digest"),
        ),
        _check(
            "identity_plan_candidate_digest_bound",
            candidate_service.EXPECTED_IDENTITY_AUTHORITY_PLAN_CANDIDATE_DIGEST,
            review_package.get("identity_authority_plan_candidate_digest"),
        ),
        _check(
            "live_validation_results_review_digest_bound",
            candidate_service.plan_review.plan.EXPECTED_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_DIGEST,
            review_package.get("live_ticker_validation_results_review_package_digest"),
        ),
        _check(
            "live_validation_execution_digest_bound",
            candidate_service.plan_review.plan.EXPECTED_LIVE_TICKER_VALIDATION_EXECUTION_DIGEST,
            review_package.get("live_ticker_validation_execution_digest"),
        ),
        _check(
            "live_validation_approval_digest_bound",
            candidate_service.plan_review.plan.EXPECTED_LIVE_TICKER_VALIDATION_APPROVAL_DIGEST,
            review_package.get("live_ticker_validation_approval_digest"),
        ),
        _check(
            "ticker_universe_selection_approval_digest_bound",
            candidate_service.plan_review.plan.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST,
            review_package.get("ticker_universe_selection_approval_digest"),
        ),
        _check("target_universe_count_12", 12, review_package.get("target_universe_count")),
        _check(
            "target_universe_matches_validated_universe",
            True,
            review_package.get("target_universe")
            == review_package.get("validated_universe")
            == VALIDATION_TARGET_UNIVERSE,
        ),
        _check(
            "all_targets_validated_read_only",
            True,
            review_package.get("all_targets_validated_read_only"),
        ),
        _check(
            "identity_review_scope_review_only_not_freeze",
            REVIEW_ONLY_NOT_FREEZE,
            review_package.get("identity_authority_candidate_review_scope"),
        ),
        _check("per_ticker_identity_candidate_entries_12", 12, len(candidate_entries)),
        _check("per_ticker_identity_review_entries_12", 12, len(review_entries)),
        _check(
            "per_ticker_identity_review_status_ready",
            True,
            len(review_entries) == 12
            and all(
                entry.get("per_ticker_identity_review_status")
                == READY_FOR_OPERATOR_ASSESSMENT
                for entry in review_entries
            ),
        ),
        _check(
            "per_ticker_identity_authority_created_false",
            True,
            len(review_entries) == 12
            and all(entry.get("identity_authority_created") is False for entry in review_entries),
        ),
        _check(
            "per_ticker_identity_freeze_status_not_frozen",
            True,
            len(review_entries) == 12
            and all(
                entry.get("identity_freeze_status")
                == candidate_service.plan_review.plan.NOT_FROZEN
                for entry in review_entries
            ),
        ),
        _check("identity_fields_to_bind_reviewed", IDENTITY_FIELDS_TO_BIND, review_package.get("identity_fields_to_bind")),
        _check(
            "identity_fields_use_status_value_structure",
            True,
            _identity_fields_have_value_status(review_entries),
        ),
        _check(
            "unavailable_fields_marked_unavailable_not_fabricated",
            True,
            _unavailable_fields_not_fabricated(review_entries),
        ),
        _check(
            "provider_response_digest_bound_or_marked_unavailable",
            True,
            _digest_field_bound_or_unavailable(review_entries, "provider_response_digest"),
        ),
        _check(
            "sanitized_validation_digest_bound_or_marked_unavailable",
            True,
            _digest_field_bound_or_unavailable(review_entries, "sanitized_validation_digest"),
        ),
        _check(
            "per_ticker_identity_candidate_digests_present",
            True,
            len(review_entries) == 12
            and all(entry.get("per_ticker_identity_candidate_digest") for entry in review_entries),
        ),
        _check(
            "per_ticker_identity_review_digests_present",
            True,
            len(review_entries) == 12
            and all(entry.get("per_ticker_identity_review_digest") for entry in review_entries),
        ),
        _check("identity_field_classification_reviewed", IDENTITY_FIELD_GROUPS, review_package.get("identity_field_groups")),
        _check(
            "identity_evidence_limitations_recorded",
            IDENTITY_EVIDENCE_LIMITATIONS,
            review_package.get("identity_evidence_limitations"),
        ),
        _check(
            "future_identity_authority_chain_defined",
            _future_identity_authority_chain(),
            review_package.get("future_identity_authority_chain"),
        ),
        _check("future_gates_defined", FUTURE_GATES, review_package.get("future_gates")),
        _check("risk_controls_defined", RISK_CONTROLS, review_package.get("risk_controls")),
        _check("provider_requests_made_in_review_false", False, review_package.get("provider_requests_made_in_review")),
        _check("live_validation_rerun_performed_false", False, review_package.get("live_validation_rerun_performed")),
        _check(
            "live_provider_transport_enabled_in_review_false",
            False,
            review_package.get("live_provider_transport_enabled_in_review"),
        ),
        _check(
            "per_ticker_identity_authority_frozen_false",
            False,
            review_package.get("per_ticker_identity_authority_frozen"),
        ),
        _check("identity_authority_created_false", False, review_package.get("identity_authority_created")),
        _check("new_ticker_authority_created_false", False, review_package.get("new_ticker_authority_created")),
        _check("new_ticker_acquisition_authorized_false", False, review_package.get("new_ticker_acquisition_authorized")),
        _check("dataset_generation_authorized_false", False, review_package.get("dataset_generation_authorized")),
        _check("corporate_action_authority_created_false", False, review_package.get("corporate_action_authority_created")),
        _check("split_event_authority_created_false", False, review_package.get("split_event_authority_created")),
        _check("dividend_event_authority_created_false", False, review_package.get("dividend_event_authority_created")),
        _check("acquisition_generation_authorized_false", False, review_package.get("acquisition_generation_authorized")),
        _check("canonical_dataset_authorized_false", False, review_package.get("canonical_dataset_authorized")),
        _check("registry_approval_created_false", False, review_package.get("registry_approval_created")),
        _check(
            "additional_predictive_evidence_execution_authorized_false",
            False,
            review_package.get("additional_predictive_evidence_execution_authorized"),
        ),
        _check(
            "additional_predictive_evidence_executed_false",
            False,
            review_package.get("additional_predictive_evidence_executed"),
        ),
        _check("predictive_experiment_rerun_authorized_false", False, review_package.get("predictive_experiment_rerun_authorized")),
        _check("predictive_experiment_rerun_performed_false", False, review_package.get("predictive_experiment_rerun_performed")),
        _check("walk_forward_rerun_performed_false", False, review_package.get("walk_forward_rerun_performed")),
        _check("label_regeneration_performed_false", False, review_package.get("label_regeneration_performed")),
        _check("feature_matrix_regeneration_performed_false", False, review_package.get("feature_matrix_regeneration_performed")),
        _check("new_strategy_scoring_performed_false", False, review_package.get("new_strategy_scoring_performed")),
        _check("trade_recommendations_generated_false", False, review_package.get("trade_recommendations_generated")),
        _check(
            "predictive_usefulness_not_accepted",
            acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
            review_package.get("predictive_usefulness"),
        ),
        _check("predictive_usefulness_acceptance_ready_false", False, review_package.get("predictive_usefulness_acceptance_ready")),
        _check(
            "predictive_usefulness_acceptance_recommended_false",
            False,
            review_package.get("predictive_usefulness_acceptance_recommended"),
        ),
        _check(
            "predictive_usefulness_acceptance_candidate_created_false",
            False,
            review_package.get("predictive_usefulness_acceptance_candidate_created"),
        ),
        _check("profitability_not_accepted", acquisition.PROFITABILITY_NOT_ACCEPTED, review_package.get("profitability")),
        _check("profitability_acceptance_ready_false", False, review_package.get("profitability_acceptance_ready")),
        _check("profitability_acceptance_recommended_false", False, review_package.get("profitability_acceptance_recommended")),
        _check("runtime_migration_recommended_false", False, review_package.get("runtime_migration_recommended")),
        _check("runtime_migration_approved_false", False, review_package.get("runtime_migration_approved")),
        _check("runtime_migration_active_false", False, review_package.get("runtime_migration_active")),
        _check("strategy_runtime_migration_false", False, review_package.get("strategy_runtime_migration")),
        _check("runtime_use_not_authorized", candidate_service.plan_review.plan.NOT_AUTHORIZED, review_package.get("runtime_use")),
        _check("strategy_use_not_authorized", candidate_service.plan_review.plan.NOT_AUTHORIZED, review_package.get("strategy_use")),
        _check("paper_trading_not_authorized", candidate_service.plan_review.plan.NOT_AUTHORIZED, review_package.get("paper_trading")),
        _check("broker_execution_not_authorized", candidate_service.plan_review.plan.NOT_AUTHORIZED, review_package.get("broker_execution")),
        _check("automatic_stitching_false", False, review_package.get("automatic_stitching")),
        _check("no_identity_authority_freeze_created", False, review_package.get("identity_authority_freeze_created")),
        _check("no_corporate_action_authority_created", False, review_package.get("corporate_action_authority_created")),
        _check("no_acquisition_authorization_created", False, review_package.get("acquisition_authorization_created")),
        _check(
            "no_dataset_generation_authorization_created",
            False,
            review_package.get("dataset_generation_authorization_created"),
        ),
        _check(
            "no_predictive_usefulness_acceptance_artifact_created",
            False,
            review_package.get("predictive_usefulness_acceptance_artifact_created"),
        ),
        _check("no_profitability_acceptance_created", False, review_package.get("profitability_acceptance_created")),
        _check("no_runtime_migration_approval_created", False, review_package.get("runtime_migration_approval_created")),
    ]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [item for item in checklist if item["status"] != PASS]
    blocker_count = sum(1 for item in failed if item.get("severity") == BLOCKER)
    return {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": blocker_count,
        "ready_for_operator_assessment": not failed,
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


def _digest_payload(review_package: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(review_package)
    payload.pop(
        "expanded_universe_per_ticker_identity_authority_candidate_review_package_digest",
        None,
    )
    return payload


def expanded_universe_per_ticker_identity_authority_candidate_review_package_digest_v1(
    review_package: dict[str, Any],
) -> str:
    """Return the deterministic semantic digest for the candidate review package."""
    return semantic_digest(_digest_payload(review_package))


def build_expanded_universe_per_ticker_identity_authority_candidate_review_package_v1(
    candidate: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build the offline candidate review package without freezing identity."""
    bound_candidate, binding_mode = _candidate_for_binding(candidate)
    review_package = _base_review_package(bound_candidate, binding_mode)
    checklist = _checklist(review_package)
    review_package["review_checklist"] = checklist
    review_package["review_summary"] = _summary(checklist)
    review_package[
        "expanded_universe_per_ticker_identity_authority_candidate_review_package_digest"
    ] = expanded_universe_per_ticker_identity_authority_candidate_review_package_digest_v1(
        review_package
    )
    validate_expanded_universe_per_ticker_identity_authority_candidate_review_package_v1(
        review_package
    )
    return review_package


def _reject_forbidden_values(mapping: dict[str, Any], *, path: str = "review_package") -> None:
    forbidden_true_fields = {
        "provider_requests_made_in_review",
        "live_validation_rerun_performed",
        "live_provider_transport_enabled_in_review",
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
        if key == "artifact_kind" and path != "review_package":
            raise ExpandedUniversePerTickerIdentityAuthorityCandidateReviewPackageError(
                f"{current_path} must not create another artifact kind"
            )
        if key in forbidden_true_fields and value is True:
            raise ExpandedUniversePerTickerIdentityAuthorityCandidateReviewPackageError(
                f"{current_path} must be false"
            )
        if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"}:
            if value == "AUTHORIZED":
                raise ExpandedUniversePerTickerIdentityAuthorityCandidateReviewPackageError(
                    f"{current_path} must not be AUTHORIZED"
                )
        if key in {"predictive_usefulness", "profitability"} and value == "accepted":
            raise ExpandedUniversePerTickerIdentityAuthorityCandidateReviewPackageError(
                f"{current_path} must not be accepted"
            )
        if isinstance(value, dict):
            _reject_forbidden_values(value, path=current_path)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, dict):
                    _reject_forbidden_values(item, path=f"{current_path}[{index}]")


def _validate_review_entries(review_package: dict[str, Any]) -> None:
    candidate_entries = _candidate_entries(review_package)
    review_entries = _review_entries_from_package(review_package)
    if len(candidate_entries) != 12:
        raise ExpandedUniversePerTickerIdentityAuthorityCandidateReviewPackageError(
            "per_ticker_identity_candidate_entries mismatch"
        )
    if len(review_entries) != 12:
        raise ExpandedUniversePerTickerIdentityAuthorityCandidateReviewPackageError(
            "per_ticker_identity_review_entries mismatch"
        )
    _expect(
        [entry.get("ticker") for entry in review_entries],
        VALIDATION_TARGET_UNIVERSE,
        "per_ticker_identity_review_entries tickers",
    )
    if not _identity_fields_have_value_status(review_entries):
        raise ExpandedUniversePerTickerIdentityAuthorityCandidateReviewPackageError(
            "identity fields must use value/status structure"
        )
    if not _unavailable_fields_not_fabricated(review_entries):
        raise ExpandedUniversePerTickerIdentityAuthorityCandidateReviewPackageError(
            "unavailable identity fields must not be fabricated"
        )
    for entry in review_entries:
        ticker = entry.get("ticker")
        _expect(
            entry.get("identity_candidate_status"),
            candidate_service.IDENTITY_CANDIDATE_READY_FOR_OPERATOR_REVIEW,
            f"{ticker}.identity_candidate_status",
        )
        _expect(
            entry.get("identity_review_status"),
            REVIEW_PACKAGE_CREATED,
            f"{ticker}.identity_review_status",
        )
        _expect(
            entry.get("identity_authority_scope"),
            CANDIDATE_REVIEW_ONLY_NOT_FROZEN,
            f"{ticker}.identity_authority_scope",
        )
        _expect_false(entry.get("identity_authority_created"), f"{ticker}.identity_authority_created")
        _expect(
            entry.get("identity_freeze_status"),
            candidate_service.plan_review.plan.NOT_FROZEN,
            f"{ticker}.identity_freeze_status",
        )
        _expect(
            entry.get("identity_evidence_limitations"),
            IDENTITY_EVIDENCE_LIMITATIONS,
            f"{ticker}.identity_evidence_limitations",
        )
        candidate_digest = entry.get("per_ticker_identity_candidate_digest")
        if not isinstance(candidate_digest, str) or len(candidate_digest) != 64:
            raise ExpandedUniversePerTickerIdentityAuthorityCandidateReviewPackageError(
                "per_ticker_identity_candidate_digest missing"
            )
        _expect(
            entry.get("per_ticker_identity_review_status"),
            READY_FOR_OPERATOR_ASSESSMENT,
            f"{ticker}.per_ticker_identity_review_status",
        )
        review_digest = entry.get("per_ticker_identity_review_digest")
        if not isinstance(review_digest, str) or len(review_digest) != 64:
            raise ExpandedUniversePerTickerIdentityAuthorityCandidateReviewPackageError(
                "per_ticker_identity_review_digest missing"
            )
        _expect(
            review_digest,
            per_ticker_identity_review_digest_v1(entry),
            f"{ticker}.per_ticker_identity_review_digest",
        )


def validate_expanded_universe_per_ticker_identity_authority_candidate_review_package_v1(
    review_package: dict[str, Any],
) -> dict[str, Any]:
    """Validate the review package without freezing identity or expanding authority."""
    if not isinstance(review_package, dict):
        raise ExpandedUniversePerTickerIdentityAuthorityCandidateReviewPackageError(
            "review_package must be a JSON object"
        )
    _reject_forbidden_values(review_package)
    _expect(
        review_package.get("artifact_kind"),
        ARTIFACT_KIND_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_CANDIDATE_REVIEW_PACKAGE,
        "artifact_kind",
    )
    _expect(
        review_package.get("schema_version"),
        SCHEMA_VERSION_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_CANDIDATE_REVIEW_V1,
        "schema_version",
    )
    _expect(
        review_package.get("review_status"),
        EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_READY,
        "review_status",
    )
    if review_package.get("identity_authority_candidate_binding_mode") not in {
        EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_CANDIDATE_STATUS_BINDING,
        EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_CANDIDATE_OBJECT_BINDING,
    }:
        raise ExpandedUniversePerTickerIdentityAuthorityCandidateReviewPackageError(
            "identity_authority_candidate_binding_mode mismatch"
        )
    expected_candidate_digest = (
        EXPECTED_IDENTITY_AUTHORITY_CANDIDATE_DIGEST
        if review_package.get("identity_authority_candidate_binding_mode")
        == EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_CANDIDATE_STATUS_BINDING
        else review_package.get("identity_authority_candidate_digest")
    )
    if not isinstance(expected_candidate_digest, str) or len(expected_candidate_digest) != 64:
        raise ExpandedUniversePerTickerIdentityAuthorityCandidateReviewPackageError(
            "identity_authority_candidate_digest missing"
        )
    _expect(
        review_package.get("reviewed_identity_authority_candidate_digest"),
        expected_candidate_digest,
        "reviewed_identity_authority_candidate_digest",
    )
    _expect(
        review_package.get("identity_authority_candidate_digest"),
        expected_candidate_digest,
        "identity_authority_candidate_digest",
    )
    for field in (
        "operator_decision_required",
        "created_offline",
        "per_ticker_identity_authority_candidate_created",
        "per_ticker_identity_authority_review_created",
        "research_only",
    ):
        _expect_true(review_package.get(field), field)
    _expect(review_package.get("operator_decision"), None, "operator_decision")
    for field in (
        "provider_requests_made_in_review",
        "live_validation_rerun_performed",
        "live_provider_transport_enabled_in_review",
        "source_output_file_reinspection_performed",
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
        "identity_authority_freeze_created",
        "corporate_action_authority_authorized",
        "acquisition_authorized",
        "acquisition_authorization_created",
        "dataset_generation_authorization_created",
        "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_created",
        "runtime_migration_approval_created",
    ):
        _expect_false(review_package.get(field), field)
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(review_package.get(field), candidate_service.plan_review.plan.NOT_AUTHORIZED, field)
    for field, expected in {
        "identity_authority_candidate_review_scope": REVIEW_ONLY_NOT_FREEZE,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "reviewed_identity_authority_candidate_kind": (
            candidate_service.ARTIFACT_KIND_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_CANDIDATE
        ),
        "reviewed_identity_authority_candidate_status": (
            candidate_service.EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_READY_FOR_OPERATOR_REVIEW
        ),
        "reviewed_identity_authority_candidate_checklist_total": (
            EXPECTED_REVIEWED_IDENTITY_AUTHORITY_CANDIDATE_CHECKLIST_TOTAL
        ),
        "reviewed_identity_authority_candidate_checklist_passed": (
            EXPECTED_REVIEWED_IDENTITY_AUTHORITY_CANDIDATE_CHECKLIST_PASSED
        ),
        "reviewed_identity_authority_candidate_checklist_failed": (
            EXPECTED_REVIEWED_IDENTITY_AUTHORITY_CANDIDATE_CHECKLIST_FAILED
        ),
        "reviewed_identity_authority_candidate_blocker_count": (
            EXPECTED_REVIEWED_IDENTITY_AUTHORITY_CANDIDATE_BLOCKER_COUNT
        ),
        "identity_authority_plan_candidate_review_package_digest": (
            candidate_service.EXPECTED_IDENTITY_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "identity_authority_plan_candidate_digest": (
            candidate_service.EXPECTED_IDENTITY_AUTHORITY_PLAN_CANDIDATE_DIGEST
        ),
        "live_ticker_validation_results_review_package_digest": (
            candidate_service.plan_review.plan.EXPECTED_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_DIGEST
        ),
        "live_ticker_validation_execution_digest": (
            candidate_service.plan_review.plan.EXPECTED_LIVE_TICKER_VALIDATION_EXECUTION_DIGEST
        ),
        "live_ticker_validation_approval_digest": (
            candidate_service.plan_review.plan.EXPECTED_LIVE_TICKER_VALIDATION_APPROVAL_DIGEST
        ),
        "live_ticker_validation_candidate_digest": (
            candidate_service.plan_review.plan.EXPECTED_LIVE_TICKER_VALIDATION_CANDIDATE_DIGEST
        ),
        "live_ticker_validation_candidate_review_package_digest": (
            candidate_service.plan_review.plan.EXPECTED_LIVE_TICKER_VALIDATION_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "ticker_universe_selection_approval_digest": (
            candidate_service.plan_review.plan.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST
        ),
        "ticker_universe_selection_candidate_digest": (
            candidate_service.plan_review.plan.EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_DIGEST
        ),
        "ticker_universe_selection_candidate_review_package_digest": (
            candidate_service.plan_review.plan.EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "target_universe": VALIDATION_TARGET_UNIVERSE,
        "validated_universe": VALIDATION_TARGET_UNIVERSE,
        "target_universe_count": 12,
        "all_targets_validated_read_only": True,
        "validated_read_only_count": 12,
        "provider_request_count": 12,
        "successful_provider_response_count": 12,
        "failed_provider_response_count": 0,
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
        } and not review_package.get(field):
            raise ExpandedUniversePerTickerIdentityAuthorityCandidateReviewPackageError(
                f"{field} missing"
            )
        _expect(review_package.get(field), expected, field)
    if review_package.get("target_universe") != review_package.get("validated_universe"):
        raise ExpandedUniversePerTickerIdentityAuthorityCandidateReviewPackageError(
            "target universe differs from validated universe"
        )
    _validate_review_entries(review_package)
    checklist = review_package.get("review_checklist")
    if not isinstance(checklist, list):
        raise ExpandedUniversePerTickerIdentityAuthorityCandidateReviewPackageError(
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
        raise ExpandedUniversePerTickerIdentityAuthorityCandidateReviewPackageError(
            f"review checklist contains failed check: {failed[0]['check_id']}"
        )
    _expect(checklist, expected_checklist, "review_checklist")
    _expect(review_package.get("review_summary"), _summary(expected_checklist), "review_summary")
    digest = review_package.get(
        "expanded_universe_per_ticker_identity_authority_candidate_review_package_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise ExpandedUniversePerTickerIdentityAuthorityCandidateReviewPackageError(
            "expanded_universe_per_ticker_identity_authority_candidate_review_package_digest missing"
        )
    _expect(
        digest,
        expanded_universe_per_ticker_identity_authority_candidate_review_package_digest_v1(
            review_package
        ),
        "expanded_universe_per_ticker_identity_authority_candidate_review_package_digest",
    )
    return {
        "status": "EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_VALID",
        "artifact_kind": review_package["artifact_kind"],
        "review_status": review_package["review_status"],
        "expanded_universe_per_ticker_identity_authority_candidate_review_package_digest": (
            digest
        ),
        "reviewed_identity_authority_candidate_digest": review_package[
            "reviewed_identity_authority_candidate_digest"
        ],
        "identity_authority_plan_candidate_review_package_digest": review_package[
            "identity_authority_plan_candidate_review_package_digest"
        ],
        "live_ticker_validation_results_review_package_digest": review_package[
            "live_ticker_validation_results_review_package_digest"
        ],
        "target_universe_count": review_package["target_universe_count"],
        "per_ticker_identity_review_entry_count": len(_review_entries_from_package(review_package)),
        "total_checks": review_package["review_summary"]["total_checks"],
        "passed_checks": review_package["review_summary"]["passed_checks"],
        "failed_checks": review_package["review_summary"]["failed_checks"],
        "blocker_count": review_package["review_summary"]["blocker_count"],
        "ready_for_operator_assessment": review_package["review_summary"][
            "ready_for_operator_assessment"
        ],
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


def build_expanded_universe_per_ticker_identity_authority_candidate_review_markdown_v1(
    review_package: dict[str, Any],
) -> str:
    """Render a sanitized candidate review package status document."""
    validation = validate_expanded_universe_per_ticker_identity_authority_candidate_review_package_v1(
        review_package
    )
    summary = review_package["review_summary"]
    unavailable_fields = sorted(
        {
            field_name
            for entry in _review_entries_from_package(review_package)
            for field_name, field in entry.get("identity_fields", {}).items()
            if isinstance(field, dict)
            and field.get("status") == candidate_service.UNAVAILABLE_IN_SOURCE
        }
    )
    lines = [
        "# MarketFlow Expanded Universe Per-Ticker Identity Authority Candidate Operator Review Package Status",
        "",
        "## Title",
        "- Expanded Universe Per-Ticker Identity Authority Candidate Operator Review Package v1.",
        "",
        "## Reviewed Expanded Universe Identity Authority Candidate",
        f"- Candidate kind: `{review_package['reviewed_identity_authority_candidate_kind']}`",
        f"- Candidate status: `{review_package['reviewed_identity_authority_candidate_status']}`",
        f"- Candidate digest: `{review_package['reviewed_identity_authority_candidate_digest']}`",
        f"- Review package digest: `{validation['expanded_universe_per_ticker_identity_authority_candidate_review_package_digest']}`",
        "",
        "## Source Identity Candidate",
        f"- Identity candidate digest: `{review_package['identity_authority_candidate_digest']}`",
        f"- Plan review digest: `{review_package['identity_authority_plan_candidate_review_package_digest']}`",
        "",
        "## Source Live Ticker Validation Evidence",
        f"- Live ticker validation results review package digest: `{review_package['live_ticker_validation_results_review_package_digest']}`",
        f"- Live ticker validation execution digest: `{review_package['live_ticker_validation_execution_digest']}`",
        f"- Live ticker validation approval digest: `{review_package['live_ticker_validation_approval_digest']}`",
        "",
        "## Target Universe",
        f"- Target universe count: `{review_package['target_universe_count']}`",
        "- Target universe: " + ", ".join(f"`{ticker}`" for ticker in review_package["target_universe"]),
        "",
        "## Per-Ticker Identity Review Summary",
    ]
    lines.extend(
        f"- `{entry['ticker']}`: `{entry['per_ticker_identity_review_status']}`, freeze `{entry['identity_freeze_status']}`, review digest `{entry['per_ticker_identity_review_digest']}`"
        for entry in _review_entries_from_package(review_package)
    )
    lines.extend(["", "## Identity Fields Reviewed"])
    lines.extend(f"- `{field}`" for field in review_package["identity_fields_to_bind"])
    lines.extend(["", "## Unavailable Fields and Limitations"])
    lines.extend(f"- `{field}`" for field in unavailable_fields)
    lines.extend(f"- `{item}`" for item in review_package["identity_evidence_limitations"])
    lines.extend(["", "## Future Identity Authority Chain"])
    lines.extend(
        f"- `{step['step_number']}`: {step['authority_step']}"
        for step in review_package["future_identity_authority_chain"]
    )
    lines.extend(["", "## Future Gates"])
    lines.extend(f"- `{gate}`" for gate in review_package["future_gates"])
    lines.extend(["", "## Risk Controls"])
    lines.extend(f"- `{control}`" for control in review_package["risk_controls"])
    lines.extend(
        [
            "",
            "## Authority Boundary",
            f"- identity_authority_candidate_review_scope: `{review_package['identity_authority_candidate_review_scope']}`",
            f"- per_ticker_identity_authority_candidate_created: `{review_package['per_ticker_identity_authority_candidate_created']}`",
            f"- per_ticker_identity_authority_review_created: `{review_package['per_ticker_identity_authority_review_created']}`",
            f"- per_ticker_identity_authority_frozen: `{review_package['per_ticker_identity_authority_frozen']}`",
            f"- identity_authority_created: `{review_package['identity_authority_created']}`",
            f"- new_ticker_authority_created: `{review_package['new_ticker_authority_created']}`",
            "",
            "## Acquisition Boundary",
            f"- new_ticker_acquisition_authorized: `{review_package['new_ticker_acquisition_authorized']}`",
            f"- acquisition_generation_authorized: `{review_package['acquisition_generation_authorized']}`",
            "",
            "## Dataset Boundary",
            f"- dataset_generation_authorized: `{review_package['dataset_generation_authorized']}`",
            f"- canonical_dataset_authorized: `{review_package['canonical_dataset_authorized']}`",
            "",
            "## Predictive/Profitability Boundary",
            f"- additional_predictive_evidence_execution_authorized: `{review_package['additional_predictive_evidence_execution_authorized']}`",
            f"- additional_predictive_evidence_executed: `{review_package['additional_predictive_evidence_executed']}`",
            f"- predictive_usefulness: `{review_package['predictive_usefulness']}`",
            f"- profitability: `{review_package['profitability']}`",
            "",
            "## Runtime Boundary",
            f"- runtime_migration_approved: `{review_package['runtime_migration_approved']}`",
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
            f"- Ready for identity freeze: `{summary['ready_for_identity_freeze']}`",
            "",
            "## Guardrails",
            "- No Massive.com / Polygon provider request was made.",
            "- No live ticker validation rerun was performed.",
            "- No live provider transport was enabled in review.",
            "- No identity freeze or final identity authority was created.",
            "- No corporate-action, acquisition, dataset, predictive, profitability, runtime, paper-trading, broker, or trade-recommendation authorization was created.",
            "",
        ]
    )
    return "\n".join(lines)


def write_expanded_universe_per_ticker_identity_authority_candidate_review_package_v1(
    output_dir: str | Path,
    *,
    candidate: dict[str, Any] | None = None,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write the candidate review package JSON without overwriting output."""
    review_package = build_expanded_universe_per_ticker_identity_authority_candidate_review_package_v1(
        candidate=candidate
    )
    validation = validate_expanded_universe_per_ticker_identity_authority_candidate_review_package_v1(
        review_package
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = (
        filename
        or "expanded_universe_per_ticker_identity_authority_candidate_review_package_v1.json"
    )
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise ExpandedUniversePerTickerIdentityAuthorityCandidateReviewPackageError(
            "expanded universe identity authority candidate review filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise ExpandedUniversePerTickerIdentityAuthorityCandidateReviewPackageError(
            "expanded universe identity authority candidate review output already exists"
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
