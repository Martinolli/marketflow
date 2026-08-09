"""Offline expanded-universe per-ticker identity authority plan candidate."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import live_ticker_validation_results_review_service as results_review


ARTIFACT_KIND_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_CANDIDATE = (
    "EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_CANDIDATE"
)
SCHEMA_VERSION_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_CANDIDATE_V1 = (
    "expanded_universe_per_ticker_identity_authority_plan_candidate_v1"
)
EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_READY_FOR_OPERATOR_REVIEW = (
    "EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_READY_FOR_OPERATOR_REVIEW"
)

EXPECTED_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_DIGEST = (
    "ebaa8b85894ec0eb6b29571c4f473d21b346d86e092a4e68158a401cb9ff7033"
)
EXPECTED_LIVE_TICKER_VALIDATION_EXECUTION_DIGEST = results_review.EXPECTED_SOURCE_EXECUTION_DIGEST
EXPECTED_LIVE_TICKER_VALIDATION_APPROVAL_DIGEST = (
    results_review.EXPECTED_SOURCE_EXECUTION_APPROVAL_DIGEST
)
EXPECTED_LIVE_TICKER_VALIDATION_CANDIDATE_DIGEST = results_review.EXPECTED_SOURCE_CANDIDATE_DIGEST
EXPECTED_LIVE_TICKER_VALIDATION_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    results_review.EXPECTED_SOURCE_CANDIDATE_REVIEW_PACKAGE_DIGEST
)
EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST = (
    results_review.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST
)
EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_DIGEST = (
    "6baeb13550814f8c0d3d0a815a797e2f7b46552fa2fa5aa3aa950a7f6d5fce01"
)
EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    "df63f64a3b145740a650ecf7db703356f3ee24e0dbdfdc4ac27a1812b75dcf4a"
)
EXPECTED_PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    "c94fd093f1e221e9dca127e44a3a788880602c570e9051b6e19666f1db142156"
)
EXPECTED_PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_CANDIDATE_DIGEST = (
    "daddabc04829ac2379c4439220d018d8b3b3403c35edb469e95e7b24ea6bd13f"
)
EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    "24b19efc1fdb4cbf64c02f15011becd1872301efe596a4d8bb7989f8be299b8a"
)
EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE_DIGEST = (
    "af23d2de4b77470f5d60622704312eee28fb857ebd9dfe81c1b288932cd6430f"
)

VALIDATION_TARGET_UNIVERSE = list(results_review.VALIDATION_TARGET_UNIVERSE)
VALIDATED_READ_ONLY = results_review.VALIDATED_READ_ONLY
NOT_EVALUATED_BY_SELECTED_ENDPOINT = results_review.NOT_EVALUATED_BY_SELECTED_ENDPOINT
NOT_AUTHORIZED = results_review.NOT_AUTHORIZED
RESEARCH_ONLY_NON_ACTIONABLE = results_review.RESEARCH_ONLY_NON_ACTIONABLE
PLANNED_NOT_CREATED = "PLANNED_NOT_CREATED"
NOT_CREATED = "NOT_CREATED"
NOT_FROZEN = "NOT_FROZEN"
PLANNED_NOT_GENERATED = "PLANNED_NOT_GENERATED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

IDENTITY_AUTHORITY_PLAN_OBJECTIVE = (
    "PLAN_PER_TICKER_IDENTITY_AUTHORITY_FOR_VALIDATED_EXPANDED_UNIVERSE"
)
IDENTITY_EVIDENCE_SOURCE = results_review.ARTIFACT_KIND_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE
NEXT_REQUIRED_IDENTITY_GATE = "PER_TICKER_IDENTITY_AUTHORITY_CANDIDATE"

IDENTITY_FIELDS_TO_BIND = [
    "ticker",
    "provider_canonical_ticker_if_available",
    "provider_name_if_available",
    "security_type_if_available",
    "market_if_available",
    "locale_if_available",
    "primary_exchange_if_available",
    "active_status_if_available",
    "currency_if_available",
    "cik_if_available",
    "composite_figi_if_available",
    "share_class_figi_if_available",
    "source_endpoint",
    "provider_response_digest",
    "sanitized_validation_digest",
]

IDENTITY_FIELD_GROUPS = {
    "core_symbol_identity_fields": ["ticker", "provider_canonical_ticker_if_available"],
    "provider_reference_identity_fields": [
        "provider_name_if_available",
        "source_endpoint",
        "active_status_if_available",
    ],
    "security_classification_fields": [
        "security_type_if_available",
        "market_if_available",
        "locale_if_available",
    ],
    "exchange_and_market_fields": [
        "primary_exchange_if_available",
        "currency_if_available",
    ],
    "provider_cross_reference_fields": [
        "cik_if_available",
        "composite_figi_if_available",
        "share_class_figi_if_available",
    ],
    "audit_digest_fields": ["provider_response_digest", "sanitized_validation_digest"],
    "limitation_fields": [
        "source_endpoint",
        "corporate_action_availability_not_evaluated_by_selected_endpoint",
        "historical_aggregate_availability_not_evaluated_by_selected_endpoint",
    ],
}

IDENTITY_EVIDENCE_LIMITATIONS = [
    "reference_details_only",
    "corporate_action_availability_not_evaluated_by_selected_endpoint",
    "historical_aggregate_availability_not_evaluated_by_selected_endpoint",
    "identity_freeze_not_created",
]

FUTURE_IDENTITY_AUTHORITY_CHAIN = [
    "Per-ticker identity authority candidate.",
    "Per-ticker identity candidate operator review package.",
    "Identity evidence discrepancy triage, if required.",
    "Per-ticker identity authority freeze ceremony.",
    "Post-freeze identity registry/read-only discovery.",
    "Corporate-action authority chain only after identity freeze.",
    "Acquisition generation chain only after identity and corporate-action authority.",
    "Canonical dataset chain only after acquisition freeze.",
    "Research registry approval only after canonical dataset freeze.",
]

FUTURE_GATES = [
    "expanded_universe_identity_authority_plan_operator_review",
    "per_ticker_identity_authority_candidate",
    "per_ticker_identity_authority_candidate_operator_review",
    "per_ticker_identity_authority_freeze_approval",
    "identity_discrepancy_triage_if_needed",
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
    "operator_approval_required_before_identity_authority_creation",
]

PLANNED_OUTPUT_IDS = [
    "expanded_universe_identity_authority_plan_manifest",
    "per_ticker_identity_evidence_requirement_matrix",
    "identity_field_mapping_template",
    "identity_discrepancy_triage_template",
    "per_ticker_identity_candidate_template",
    "per_ticker_identity_review_template",
    "identity_freeze_checklist_template",
    "post_identity_freeze_registry_inventory_template",
    "operator_review_summary_template",
]

REQUIRED_CHECK_IDS = [
    "live_validation_results_review_digest_bound",
    "live_validation_execution_digest_bound",
    "live_validation_approval_digest_bound",
    "ticker_universe_selection_approval_digest_bound",
    "scope_expansion_review_digest_bound",
    "target_universe_count_12",
    "target_universe_matches_validated_universe",
    "all_targets_validated_read_only",
    "validation_supports_future_authority_chain_planning_true",
    "validation_creates_new_ticker_authority_false",
    "identity_plan_objective_defined",
    "identity_authority_plan_mode_planned_not_created",
    "identity_authority_creation_status_not_created",
    "identity_freeze_status_not_frozen",
    "per_ticker_identity_plan_entries_12",
    "per_ticker_identity_candidate_not_created",
    "per_ticker_identity_review_not_created",
    "per_ticker_identity_freeze_not_created",
    "identity_fields_to_bind_defined",
    "identity_field_classification_defined",
    "identity_evidence_limitations_recorded",
    "future_identity_authority_chain_defined",
    "future_gates_defined",
    "risk_controls_defined",
    "planned_outputs_not_generated",
    "planned_outputs_research_only",
    "provider_requests_made_false",
    "live_validation_rerun_performed_false",
    "live_provider_transport_enabled_false",
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
    "no_identity_authority_candidate_created",
    "no_identity_authority_freeze_created",
    "no_corporate_action_authority_created",
    "no_acquisition_authorization_created",
    "no_dataset_generation_authorization_created",
    "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created",
    "no_runtime_migration_approval_created",
]


class ExpandedUniversePerTickerIdentityAuthorityPlanCandidateError(ValueError):
    """Raised when the expanded-universe identity authority plan violates guardrails."""


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
        raise ExpandedUniversePerTickerIdentityAuthorityPlanCandidateError(
            f"{field_name} mismatch"
        )


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise ExpandedUniversePerTickerIdentityAuthorityPlanCandidateError(
            f"{field_name} must be true"
        )


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise ExpandedUniversePerTickerIdentityAuthorityPlanCandidateError(
            f"{field_name} must be false"
        )


def _path_text(path: Path) -> str:
    return str(path).replace("\\", "/")


def _planned_outputs() -> list[dict[str, Any]]:
    return [
        {
            "output_id": output_id,
            "generation_status": PLANNED_NOT_GENERATED,
            "actionability_label": RESEARCH_ONLY_NON_ACTIONABLE,
        }
        for output_id in PLANNED_OUTPUT_IDS
    ]


def _per_ticker_identity_plan_entries() -> list[dict[str, Any]]:
    return [
        {
            "ticker": ticker,
            "live_validation_status": VALIDATED_READ_ONLY,
            "identity_authority_plan_status": PLANNED_NOT_CREATED,
            "identity_candidate_status": NOT_CREATED,
            "identity_review_status": NOT_CREATED,
            "identity_freeze_status": NOT_FROZEN,
            "identity_authority_created": False,
            "identity_fields_to_bind": list(IDENTITY_FIELDS_TO_BIND),
            "identity_evidence_source": IDENTITY_EVIDENCE_SOURCE,
            "identity_evidence_limitations": list(IDENTITY_EVIDENCE_LIMITATIONS),
            "next_required_identity_gate": NEXT_REQUIRED_IDENTITY_GATE,
        }
        for ticker in VALIDATION_TARGET_UNIVERSE
    ]


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


def _base_candidate() -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_CANDIDATE,
        "schema_version": SCHEMA_VERSION_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_CANDIDATE_V1,
        "candidate_status": (
            EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_READY_FOR_OPERATOR_REVIEW
        ),
        "created_offline": True,
        "research_only": True,
        "operator_review_required": True,
        "provider_requests_made": False,
        "live_validation_rerun_performed": False,
        "live_provider_transport_enabled": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "live_ticker_validation_results_review_package_digest": (
            EXPECTED_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_DIGEST
        ),
        "live_ticker_validation_execution_digest": (
            EXPECTED_LIVE_TICKER_VALIDATION_EXECUTION_DIGEST
        ),
        "live_ticker_validation_approval_digest": EXPECTED_LIVE_TICKER_VALIDATION_APPROVAL_DIGEST,
        "live_ticker_validation_candidate_digest": EXPECTED_LIVE_TICKER_VALIDATION_CANDIDATE_DIGEST,
        "live_ticker_validation_candidate_review_package_digest": (
            EXPECTED_LIVE_TICKER_VALIDATION_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "ticker_universe_selection_approval_digest": (
            EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST
        ),
        "ticker_universe_selection_candidate_digest": (
            EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_DIGEST
        ),
        "ticker_universe_selection_candidate_review_package_digest": (
            EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "predictive_evidence_scope_expansion_plan_candidate_review_package_digest": (
            EXPECTED_PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "predictive_evidence_scope_expansion_plan_candidate_digest": (
            EXPECTED_PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_CANDIDATE_DIGEST
        ),
        "additional_predictive_evidence_plan_candidate_review_package_digest": (
            EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "additional_predictive_evidence_plan_candidate_digest": (
            EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE_DIGEST
        ),
        "validation_target_universe": list(VALIDATION_TARGET_UNIVERSE),
        "validation_target_count": len(VALIDATION_TARGET_UNIVERSE),
        "provider_request_count": 12,
        "successful_provider_response_count": 12,
        "failed_provider_response_count": 0,
        "all_targets_validated_read_only": True,
        "validation_supports_future_authority_chain_planning": True,
        "validation_creates_new_ticker_authority": False,
        "validation_creates_acquisition_authority": False,
        "validation_creates_dataset_generation_authority": False,
        "validation_creates_predictive_evidence_authority": False,
        "corporate_action_data_availability_status": NOT_EVALUATED_BY_SELECTED_ENDPOINT,
        "historical_aggregate_data_availability_status": NOT_EVALUATED_BY_SELECTED_ENDPOINT,
        "identity_authority_plan_objective": IDENTITY_AUTHORITY_PLAN_OBJECTIVE,
        "identity_authority_plan_mode": PLANNED_NOT_CREATED,
        "identity_authority_creation_status": NOT_CREATED,
        "identity_freeze_status": NOT_FROZEN,
        "identity_authority_created": False,
        "identity_candidate_created": False,
        "identity_review_created": False,
        "identity_freeze_created": False,
        "identity_fields_to_bind": list(IDENTITY_FIELDS_TO_BIND),
        "identity_field_groups": deepcopy(IDENTITY_FIELD_GROUPS),
        "identity_evidence_limitations": list(IDENTITY_EVIDENCE_LIMITATIONS),
        "per_ticker_identity_plan_entries": _per_ticker_identity_plan_entries(),
        "future_identity_authority_chain": _future_identity_authority_chain(),
        "future_gates": list(FUTURE_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "planned_outputs": _planned_outputs(),
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
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "automatic_stitching": False,
        "identity_authority_candidate_created": False,
        "identity_authority_freeze_created": False,
        "corporate_action_authority_created_in_this_task": False,
        "acquisition_authorization_created": False,
        "dataset_generation_authorization_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
    }


def _checklist(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    entries = candidate.get("per_ticker_identity_plan_entries")
    return [
        _check(
            "live_validation_results_review_digest_bound",
            EXPECTED_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_DIGEST,
            candidate.get("live_ticker_validation_results_review_package_digest"),
        ),
        _check(
            "live_validation_execution_digest_bound",
            EXPECTED_LIVE_TICKER_VALIDATION_EXECUTION_DIGEST,
            candidate.get("live_ticker_validation_execution_digest"),
        ),
        _check(
            "live_validation_approval_digest_bound",
            EXPECTED_LIVE_TICKER_VALIDATION_APPROVAL_DIGEST,
            candidate.get("live_ticker_validation_approval_digest"),
        ),
        _check(
            "ticker_universe_selection_approval_digest_bound",
            EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST,
            candidate.get("ticker_universe_selection_approval_digest"),
        ),
        _check(
            "scope_expansion_review_digest_bound",
            EXPECTED_PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST,
            candidate.get(
                "predictive_evidence_scope_expansion_plan_candidate_review_package_digest"
            ),
        ),
        _check("target_universe_count_12", 12, candidate.get("validation_target_count")),
        _check(
            "target_universe_matches_validated_universe",
            VALIDATION_TARGET_UNIVERSE,
            candidate.get("validation_target_universe"),
        ),
        _check("all_targets_validated_read_only", True, candidate.get("all_targets_validated_read_only")),
        _check(
            "validation_supports_future_authority_chain_planning_true",
            True,
            candidate.get("validation_supports_future_authority_chain_planning"),
        ),
        _check(
            "validation_creates_new_ticker_authority_false",
            False,
            candidate.get("validation_creates_new_ticker_authority"),
        ),
        _check(
            "identity_plan_objective_defined",
            IDENTITY_AUTHORITY_PLAN_OBJECTIVE,
            candidate.get("identity_authority_plan_objective"),
        ),
        _check(
            "identity_authority_plan_mode_planned_not_created",
            PLANNED_NOT_CREATED,
            candidate.get("identity_authority_plan_mode"),
        ),
        _check(
            "identity_authority_creation_status_not_created",
            NOT_CREATED,
            candidate.get("identity_authority_creation_status"),
        ),
        _check("identity_freeze_status_not_frozen", NOT_FROZEN, candidate.get("identity_freeze_status")),
        _check(
            "per_ticker_identity_plan_entries_12",
            12,
            len(entries) if isinstance(entries, list) else None,
        ),
        _check(
            "per_ticker_identity_candidate_not_created",
            True,
            isinstance(entries, list)
            and all(item.get("identity_candidate_status") == NOT_CREATED for item in entries),
        ),
        _check(
            "per_ticker_identity_review_not_created",
            True,
            isinstance(entries, list)
            and all(item.get("identity_review_status") == NOT_CREATED for item in entries),
        ),
        _check(
            "per_ticker_identity_freeze_not_created",
            True,
            isinstance(entries, list)
            and all(item.get("identity_freeze_status") == NOT_FROZEN for item in entries),
        ),
        _check("identity_fields_to_bind_defined", IDENTITY_FIELDS_TO_BIND, candidate.get("identity_fields_to_bind")),
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
        _check("planned_outputs_not_generated", True, all(
            item.get("generation_status") == PLANNED_NOT_GENERATED
            for item in candidate.get("planned_outputs", [])
        )),
        _check("planned_outputs_research_only", True, all(
            item.get("actionability_label") == RESEARCH_ONLY_NON_ACTIONABLE
            for item in candidate.get("planned_outputs", [])
        )),
        _check("provider_requests_made_false", False, candidate.get("provider_requests_made")),
        _check("live_validation_rerun_performed_false", False, candidate.get("live_validation_rerun_performed")),
        _check("live_provider_transport_enabled_false", False, candidate.get("live_provider_transport_enabled")),
        _check("new_ticker_authority_created_false", False, candidate.get("new_ticker_authority_created")),
        _check("new_ticker_acquisition_authorized_false", False, candidate.get("new_ticker_acquisition_authorized")),
        _check("dataset_generation_authorized_false", False, candidate.get("dataset_generation_authorized")),
        _check("corporate_action_authority_created_false", False, candidate.get("corporate_action_authority_created")),
        _check("split_event_authority_created_false", False, candidate.get("split_event_authority_created")),
        _check("dividend_event_authority_created_false", False, candidate.get("dividend_event_authority_created")),
        _check("acquisition_generation_authorized_false", False, candidate.get("acquisition_generation_authorized")),
        _check("canonical_dataset_authorized_false", False, candidate.get("canonical_dataset_authorized")),
        _check("registry_approval_created_false", False, candidate.get("registry_approval_created")),
        _check("additional_predictive_evidence_execution_authorized_false", False, candidate.get("additional_predictive_evidence_execution_authorized")),
        _check("additional_predictive_evidence_executed_false", False, candidate.get("additional_predictive_evidence_executed")),
        _check("predictive_experiment_rerun_authorized_false", False, candidate.get("predictive_experiment_rerun_authorized")),
        _check("predictive_experiment_rerun_performed_false", False, candidate.get("predictive_experiment_rerun_performed")),
        _check("walk_forward_rerun_performed_false", False, candidate.get("walk_forward_rerun_performed")),
        _check("label_regeneration_performed_false", False, candidate.get("label_regeneration_performed")),
        _check("feature_matrix_regeneration_performed_false", False, candidate.get("feature_matrix_regeneration_performed")),
        _check("new_strategy_scoring_performed_false", False, candidate.get("new_strategy_scoring_performed")),
        _check("trade_recommendations_generated_false", False, candidate.get("trade_recommendations_generated")),
        _check("predictive_usefulness_not_accepted", acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED, candidate.get("predictive_usefulness")),
        _check("predictive_usefulness_acceptance_ready_false", False, candidate.get("predictive_usefulness_acceptance_ready")),
        _check("predictive_usefulness_acceptance_recommended_false", False, candidate.get("predictive_usefulness_acceptance_recommended")),
        _check("predictive_usefulness_acceptance_candidate_created_false", False, candidate.get("predictive_usefulness_acceptance_candidate_created")),
        _check("profitability_not_accepted", acquisition.PROFITABILITY_NOT_ACCEPTED, candidate.get("profitability")),
        _check("profitability_acceptance_ready_false", False, candidate.get("profitability_acceptance_ready")),
        _check("profitability_acceptance_recommended_false", False, candidate.get("profitability_acceptance_recommended")),
        _check("runtime_migration_recommended_false", False, candidate.get("runtime_migration_recommended")),
        _check("runtime_migration_approved_false", False, candidate.get("runtime_migration_approved")),
        _check("runtime_migration_active_false", False, candidate.get("runtime_migration_active")),
        _check("strategy_runtime_migration_false", False, candidate.get("strategy_runtime_migration")),
        _check("runtime_use_not_authorized", NOT_AUTHORIZED, candidate.get("runtime_use")),
        _check("strategy_use_not_authorized", NOT_AUTHORIZED, candidate.get("strategy_use")),
        _check("paper_trading_not_authorized", NOT_AUTHORIZED, candidate.get("paper_trading")),
        _check("broker_execution_not_authorized", NOT_AUTHORIZED, candidate.get("broker_execution")),
        _check("automatic_stitching_false", False, candidate.get("automatic_stitching")),
        _check("no_identity_authority_candidate_created", False, candidate.get("identity_authority_candidate_created")),
        _check("no_identity_authority_freeze_created", False, candidate.get("identity_authority_freeze_created")),
        _check("no_corporate_action_authority_created", False, candidate.get("corporate_action_authority_created_in_this_task")),
        _check("no_acquisition_authorization_created", False, candidate.get("acquisition_authorization_created")),
        _check("no_dataset_generation_authorization_created", False, candidate.get("dataset_generation_authorization_created")),
        _check("no_predictive_usefulness_acceptance_artifact_created", False, candidate.get("predictive_usefulness_acceptance_artifact_created")),
        _check("no_profitability_acceptance_created", False, candidate.get("profitability_acceptance_created")),
        _check("no_runtime_migration_approval_created", False, candidate.get("runtime_migration_approval_created")),
    ]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [item for item in checklist if item["status"] != PASS]
    blocker_count = sum(1 for item in failed if item.get("severity") == BLOCKER)
    return {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": blocker_count,
        "ready_for_operator_review": not failed,
        "ready_for_per_ticker_identity_authority_candidate": False,
        "identity_authority_created": False,
        "identity_freeze_created": False,
        "ready_for_corporate_action_authority": False,
        "ready_for_acquisition": False,
        "ready_for_dataset_generation": False,
        "ready_for_additional_predictive_evidence_execution_candidate": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def _digest_payload(candidate: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(candidate)
    payload.pop("expanded_universe_per_ticker_identity_authority_plan_candidate_digest", None)
    return payload


def expanded_universe_per_ticker_identity_authority_plan_candidate_digest_v1(
    candidate: dict[str, Any],
) -> str:
    """Return the deterministic semantic digest for the identity authority plan candidate."""
    return semantic_digest(_digest_payload(candidate))


def build_expanded_universe_per_ticker_identity_authority_plan_candidate_v1() -> dict[str, Any]:
    """Build the offline plan candidate without creating identity authority."""
    candidate = _base_candidate()
    checklist = _checklist(candidate)
    candidate["plan_checklist"] = checklist
    candidate["plan_summary"] = _summary(checklist)
    candidate["expanded_universe_per_ticker_identity_authority_plan_candidate_digest"] = (
        expanded_universe_per_ticker_identity_authority_plan_candidate_digest_v1(candidate)
    )
    validate_expanded_universe_per_ticker_identity_authority_plan_candidate_v1(candidate)
    return candidate


def _reject_forbidden_values(mapping: dict[str, Any], *, path: str = "candidate") -> None:
    forbidden_true_fields = {
        "provider_requests_made",
        "live_validation_rerun_performed",
        "live_provider_transport_enabled",
        "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
        "validation_creates_new_ticker_authority",
        "validation_creates_acquisition_authority",
        "validation_creates_dataset_generation_authority",
        "validation_creates_predictive_evidence_authority",
        "identity_authority_created",
        "identity_candidate_created",
        "identity_review_created",
        "identity_freeze_created",
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
        "identity_authority_candidate_created",
        "identity_authority_freeze_created",
        "corporate_action_authority_created_in_this_task",
        "acquisition_authorization_created",
        "dataset_generation_authorization_created",
        "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_created",
        "runtime_migration_approval_created",
    }
    for key, value in mapping.items():
        current_path = f"{path}.{key}"
        if key == "artifact_kind" and path != "candidate":
            raise ExpandedUniversePerTickerIdentityAuthorityPlanCandidateError(
                f"{current_path} must not create another artifact kind"
            )
        if key in forbidden_true_fields and value is True:
            raise ExpandedUniversePerTickerIdentityAuthorityPlanCandidateError(
                f"{current_path} must be false"
            )
        if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"}:
            if value == "AUTHORIZED":
                raise ExpandedUniversePerTickerIdentityAuthorityPlanCandidateError(
                    f"{current_path} must not be AUTHORIZED"
                )
        if key in {"predictive_usefulness", "profitability"} and value == "accepted":
            raise ExpandedUniversePerTickerIdentityAuthorityPlanCandidateError(
                f"{current_path} must not be accepted"
            )
        if isinstance(value, dict):
            _reject_forbidden_values(value, path=current_path)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, dict):
                    _reject_forbidden_values(item, path=f"{current_path}[{index}]")


def validate_expanded_universe_per_ticker_identity_authority_plan_candidate_v1(
    candidate: dict[str, Any],
) -> dict[str, Any]:
    """Validate the plan candidate without creating authority, data, or runtime artifacts."""
    if not isinstance(candidate, dict):
        raise ExpandedUniversePerTickerIdentityAuthorityPlanCandidateError(
            "candidate must be a JSON object"
        )
    _reject_forbidden_values(candidate)
    _expect(
        candidate.get("artifact_kind"),
        ARTIFACT_KIND_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_CANDIDATE,
        "artifact_kind",
    )
    _expect(
        candidate.get("schema_version"),
        SCHEMA_VERSION_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_CANDIDATE_V1,
        "schema_version",
    )
    _expect(
        candidate.get("candidate_status"),
        EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_READY_FOR_OPERATOR_REVIEW,
        "candidate_status",
    )
    for field in ("created_offline", "research_only", "operator_review_required"):
        _expect_true(candidate.get(field), field)
    for field in (
        "provider_requests_made",
        "live_validation_rerun_performed",
        "live_provider_transport_enabled",
        "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
        "validation_creates_new_ticker_authority",
        "validation_creates_acquisition_authority",
        "validation_creates_dataset_generation_authority",
        "validation_creates_predictive_evidence_authority",
        "identity_authority_created",
        "identity_candidate_created",
        "identity_review_created",
        "identity_freeze_created",
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
        "identity_authority_candidate_created",
        "identity_authority_freeze_created",
        "corporate_action_authority_created_in_this_task",
        "acquisition_authorization_created",
        "dataset_generation_authorization_created",
        "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_created",
        "runtime_migration_approval_created",
    ):
        _expect_false(candidate.get(field), field)
    _expect_true(
        candidate.get("validation_supports_future_authority_chain_planning"),
        "validation_supports_future_authority_chain_planning",
    )
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(candidate.get(field), NOT_AUTHORIZED, field)
    for field, expected in {
        "live_ticker_validation_results_review_package_digest": (
            EXPECTED_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_DIGEST
        ),
        "live_ticker_validation_execution_digest": EXPECTED_LIVE_TICKER_VALIDATION_EXECUTION_DIGEST,
        "live_ticker_validation_approval_digest": EXPECTED_LIVE_TICKER_VALIDATION_APPROVAL_DIGEST,
        "live_ticker_validation_candidate_digest": EXPECTED_LIVE_TICKER_VALIDATION_CANDIDATE_DIGEST,
        "live_ticker_validation_candidate_review_package_digest": (
            EXPECTED_LIVE_TICKER_VALIDATION_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "ticker_universe_selection_approval_digest": (
            EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST
        ),
        "ticker_universe_selection_candidate_digest": (
            EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_DIGEST
        ),
        "ticker_universe_selection_candidate_review_package_digest": (
            EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "predictive_evidence_scope_expansion_plan_candidate_review_package_digest": (
            EXPECTED_PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "predictive_evidence_scope_expansion_plan_candidate_digest": (
            EXPECTED_PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_CANDIDATE_DIGEST
        ),
        "additional_predictive_evidence_plan_candidate_review_package_digest": (
            EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "additional_predictive_evidence_plan_candidate_digest": (
            EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE_DIGEST
        ),
        "validation_target_universe": VALIDATION_TARGET_UNIVERSE,
        "validation_target_count": 12,
        "provider_request_count": 12,
        "successful_provider_response_count": 12,
        "failed_provider_response_count": 0,
        "all_targets_validated_read_only": True,
        "corporate_action_data_availability_status": NOT_EVALUATED_BY_SELECTED_ENDPOINT,
        "historical_aggregate_data_availability_status": NOT_EVALUATED_BY_SELECTED_ENDPOINT,
        "identity_authority_plan_objective": IDENTITY_AUTHORITY_PLAN_OBJECTIVE,
        "identity_authority_plan_mode": PLANNED_NOT_CREATED,
        "identity_authority_creation_status": NOT_CREATED,
        "identity_freeze_status": NOT_FROZEN,
        "identity_fields_to_bind": IDENTITY_FIELDS_TO_BIND,
        "identity_field_groups": IDENTITY_FIELD_GROUPS,
        "identity_evidence_limitations": IDENTITY_EVIDENCE_LIMITATIONS,
        "future_identity_authority_chain": _future_identity_authority_chain(),
        "future_gates": FUTURE_GATES,
        "risk_controls": RISK_CONTROLS,
        "planned_outputs": _planned_outputs(),
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
    }.items():
        _expect(candidate.get(field), expected, field)
    per_ticker = candidate.get("per_ticker_identity_plan_entries")
    if not isinstance(per_ticker, list) or len(per_ticker) != 12:
        raise ExpandedUniversePerTickerIdentityAuthorityPlanCandidateError(
            "per_ticker_identity_plan_entries mismatch"
        )
    _expect(
        [item.get("ticker") for item in per_ticker],
        VALIDATION_TARGET_UNIVERSE,
        "per_ticker_identity_plan_entries tickers",
    )
    for item in per_ticker:
        ticker = item.get("ticker")
        _expect(item.get("live_validation_status"), VALIDATED_READ_ONLY, f"{ticker}.live_validation_status")
        _expect(
            item.get("identity_authority_plan_status"),
            PLANNED_NOT_CREATED,
            f"{ticker}.identity_authority_plan_status",
        )
        _expect(item.get("identity_candidate_status"), NOT_CREATED, f"{ticker}.identity_candidate_status")
        _expect(item.get("identity_review_status"), NOT_CREATED, f"{ticker}.identity_review_status")
        _expect(item.get("identity_freeze_status"), NOT_FROZEN, f"{ticker}.identity_freeze_status")
        _expect_false(item.get("identity_authority_created"), f"{ticker}.identity_authority_created")
        _expect(item.get("identity_fields_to_bind"), IDENTITY_FIELDS_TO_BIND, f"{ticker}.identity_fields_to_bind")
        _expect(item.get("identity_evidence_source"), IDENTITY_EVIDENCE_SOURCE, f"{ticker}.identity_evidence_source")
        _expect(
            item.get("identity_evidence_limitations"),
            IDENTITY_EVIDENCE_LIMITATIONS,
            f"{ticker}.identity_evidence_limitations",
        )
        _expect(
            item.get("next_required_identity_gate"),
            NEXT_REQUIRED_IDENTITY_GATE,
            f"{ticker}.next_required_identity_gate",
        )
    checklist = candidate.get("plan_checklist")
    if not isinstance(checklist, list):
        raise ExpandedUniversePerTickerIdentityAuthorityPlanCandidateError(
            "plan_checklist missing"
        )
    _expect([item.get("check_id") for item in checklist], REQUIRED_CHECK_IDS, "plan_checklist check IDs")
    expected_checklist = _checklist(candidate)
    failed = [item for item in expected_checklist if item["status"] != PASS]
    if failed:
        raise ExpandedUniversePerTickerIdentityAuthorityPlanCandidateError(
            f"plan checklist contains failed check: {failed[0]['check_id']}"
        )
    _expect(checklist, expected_checklist, "plan_checklist")
    _expect(candidate.get("plan_summary"), _summary(expected_checklist), "plan_summary")
    digest = candidate.get("expanded_universe_per_ticker_identity_authority_plan_candidate_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise ExpandedUniversePerTickerIdentityAuthorityPlanCandidateError(
            "expanded_universe_per_ticker_identity_authority_plan_candidate_digest missing"
        )
    _expect(
        digest,
        expanded_universe_per_ticker_identity_authority_plan_candidate_digest_v1(candidate),
        "expanded_universe_per_ticker_identity_authority_plan_candidate_digest",
    )
    return {
        "status": "EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_CANDIDATE_VALID",
        "artifact_kind": candidate["artifact_kind"],
        "candidate_status": candidate["candidate_status"],
        "expanded_universe_per_ticker_identity_authority_plan_candidate_digest": digest,
        "live_ticker_validation_results_review_package_digest": candidate[
            "live_ticker_validation_results_review_package_digest"
        ],
        "validation_target_count": candidate["validation_target_count"],
        "per_ticker_identity_plan_entry_count": len(per_ticker),
        "ready_for_operator_review": candidate["plan_summary"]["ready_for_operator_review"],
        "ready_for_per_ticker_identity_authority_candidate": False,
        "identity_authority_created": False,
        "identity_freeze_created": False,
        "ready_for_acquisition": False,
        "ready_for_dataset_generation": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
    }


def build_expanded_universe_per_ticker_identity_authority_plan_candidate_markdown_v1(
    candidate: dict[str, Any],
) -> str:
    """Render a sanitized expanded-universe identity authority plan candidate summary."""
    validation = validate_expanded_universe_per_ticker_identity_authority_plan_candidate_v1(candidate)
    summary = candidate["plan_summary"]
    lines = [
        "# MarketFlow Expanded Universe Per-Ticker Identity Authority Plan Candidate Status",
        "",
        "## Title",
        "- Expanded Universe Per-Ticker Identity Authority Plan Candidate v1.",
        "",
        "## Purpose",
        "- Plan future per-ticker identity authority for the validated expanded universe.",
        "- This artifact does not create identity authority, freeze identity, refresh providers, acquire data, generate datasets, authorize runtime use, or accept predictive usefulness or profitability.",
        "",
        "## Plan Artifact",
        f"- Artifact kind: `{candidate['artifact_kind']}`",
        f"- Candidate status: `{candidate['candidate_status']}`",
        f"- Schema version: `{candidate['schema_version']}`",
        f"- Plan candidate digest: `{validation['expanded_universe_per_ticker_identity_authority_plan_candidate_digest']}`",
        "",
        "## Bound Source Evidence",
        f"- Live ticker validation results review package digest: `{candidate['live_ticker_validation_results_review_package_digest']}`",
        f"- Live ticker validation execution digest: `{candidate['live_ticker_validation_execution_digest']}`",
        f"- Live ticker validation approval digest: `{candidate['live_ticker_validation_approval_digest']}`",
        f"- Ticker universe selection approval digest: `{candidate['ticker_universe_selection_approval_digest']}`",
        f"- Predictive evidence scope expansion review package digest: `{candidate['predictive_evidence_scope_expansion_plan_candidate_review_package_digest']}`",
        "",
        "## Validated Expanded Universe",
        f"- Validation target count: `{candidate['validation_target_count']}`",
        "- Validation targets: " + ", ".join(f"`{ticker}`" for ticker in candidate["validation_target_universe"]),
        f"- Provider request count from source validation: `{candidate['provider_request_count']}`",
        f"- Successful provider response count from source validation: `{candidate['successful_provider_response_count']}`",
        f"- Failed provider response count from source validation: `{candidate['failed_provider_response_count']}`",
        f"- All targets validated read-only: `{candidate['all_targets_validated_read_only']}`",
        "",
        "## Identity Plan Boundary",
        f"- identity_authority_plan_objective: `{candidate['identity_authority_plan_objective']}`",
        f"- identity_authority_plan_mode: `{candidate['identity_authority_plan_mode']}`",
        f"- identity_authority_creation_status: `{candidate['identity_authority_creation_status']}`",
        f"- identity_freeze_status: `{candidate['identity_freeze_status']}`",
        f"- identity_authority_created: `{candidate['identity_authority_created']}`",
        "",
        "## Per-Ticker Identity Plan",
    ]
    lines.extend(
        f"- `{entry['ticker']}`: validation `{entry['live_validation_status']}`, plan `{entry['identity_authority_plan_status']}`, candidate `{entry['identity_candidate_status']}`, review `{entry['identity_review_status']}`, freeze `{entry['identity_freeze_status']}`"
        for entry in candidate["per_ticker_identity_plan_entries"]
    )
    lines.extend(["", "## Identity Fields To Bind"])
    lines.extend(f"- `{field}`" for field in candidate["identity_fields_to_bind"])
    lines.extend(["", "## Identity Field Groups"])
    lines.extend(
        f"- `{group}`: " + ", ".join(f"`{field}`" for field in fields)
        for group, fields in candidate["identity_field_groups"].items()
    )
    lines.extend(["", "## Identity Evidence Limitations"])
    lines.extend(f"- `{item}`" for item in candidate["identity_evidence_limitations"])
    lines.extend(["", "## Future Identity Authority Chain"])
    lines.extend(
        f"- `{step['step_number']}`: {step['authority_step']}"
        for step in candidate["future_identity_authority_chain"]
    )
    lines.extend(["", "## Future Gates"])
    lines.extend(f"- `{gate}`" for gate in candidate["future_gates"])
    lines.extend(["", "## Planned Outputs"])
    lines.extend(
        f"- `{item['output_id']}`: `{item['generation_status']}`, `{item['actionability_label']}`"
        for item in candidate["planned_outputs"]
    )
    lines.extend(["", "## Risk Controls"])
    lines.extend(f"- `{control}`" for control in candidate["risk_controls"])
    lines.extend(
        [
            "",
            "## Authority Boundary",
            f"- validation_supports_future_authority_chain_planning: `{candidate['validation_supports_future_authority_chain_planning']}`",
            f"- validation_creates_new_ticker_authority: `{candidate['validation_creates_new_ticker_authority']}`",
            f"- new_ticker_authority_created: `{candidate['new_ticker_authority_created']}`",
            f"- identity_authority_candidate_created: `{candidate['identity_authority_candidate_created']}`",
            f"- identity_authority_freeze_created: `{candidate['identity_authority_freeze_created']}`",
            "",
            "## Acquisition And Dataset Boundary",
            f"- new_ticker_acquisition_authorized: `{candidate['new_ticker_acquisition_authorized']}`",
            f"- acquisition_generation_authorized: `{candidate['acquisition_generation_authorized']}`",
            f"- dataset_generation_authorized: `{candidate['dataset_generation_authorized']}`",
            f"- canonical_dataset_authorized: `{candidate['canonical_dataset_authorized']}`",
            "",
            "## Predictive/Profitability Boundary",
            f"- additional_predictive_evidence_execution_authorized: `{candidate['additional_predictive_evidence_execution_authorized']}`",
            f"- additional_predictive_evidence_executed: `{candidate['additional_predictive_evidence_executed']}`",
            f"- predictive_experiment_rerun_authorized: `{candidate['predictive_experiment_rerun_authorized']}`",
            f"- predictive_experiment_rerun_performed: `{candidate['predictive_experiment_rerun_performed']}`",
            f"- predictive_usefulness: `{candidate['predictive_usefulness']}`",
            f"- predictive_usefulness_acceptance_ready: `{candidate['predictive_usefulness_acceptance_ready']}`",
            f"- predictive_usefulness_acceptance_recommended: `{candidate['predictive_usefulness_acceptance_recommended']}`",
            f"- predictive_usefulness_acceptance_candidate_created: `{candidate['predictive_usefulness_acceptance_candidate_created']}`",
            f"- profitability: `{candidate['profitability']}`",
            f"- profitability_acceptance_ready: `{candidate['profitability_acceptance_ready']}`",
            f"- profitability_acceptance_recommended: `{candidate['profitability_acceptance_recommended']}`",
            "",
            "## Runtime Boundary",
            f"- runtime_migration_recommended: `{candidate['runtime_migration_recommended']}`",
            f"- runtime_migration_approved: `{candidate['runtime_migration_approved']}`",
            f"- runtime_migration_active: `{candidate['runtime_migration_active']}`",
            f"- strategy_runtime_migration: `{candidate['strategy_runtime_migration']}`",
            f"- runtime_use: `{candidate['runtime_use']}`",
            f"- strategy_use: `{candidate['strategy_use']}`",
            f"- paper_trading: `{candidate['paper_trading']}`",
            f"- broker_execution: `{candidate['broker_execution']}`",
            f"- automatic_stitching: `{candidate['automatic_stitching']}`",
            "",
            "## Checklist Summary",
            f"- Total checks: `{summary['total_checks']}`",
            f"- Passed checks: `{summary['passed_checks']}`",
            f"- Failed checks: `{summary['failed_checks']}`",
            f"- Blocker count: `{summary['blocker_count']}`",
            f"- Ready for operator review: `{summary['ready_for_operator_review']}`",
            f"- Ready for per-ticker identity authority candidate: `{summary['ready_for_per_ticker_identity_authority_candidate']}`",
            "",
            "## Guardrails",
            "- No Massive.com / Polygon provider request was made.",
            "- No live ticker validation rerun was performed.",
            "- No identity authority candidate or identity freeze was created.",
            "- No corporate-action, acquisition, dataset, registry, predictive, profitability, runtime, paper-trading, broker, or trade-recommendation authorization was created.",
            "",
        ]
    )
    return "\n".join(lines)


def write_expanded_universe_per_ticker_identity_authority_plan_candidate_v1(
    output_dir: str | Path,
    *,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write the plan candidate JSON without overwriting an existing artifact."""
    candidate = build_expanded_universe_per_ticker_identity_authority_plan_candidate_v1()
    validation = validate_expanded_universe_per_ticker_identity_authority_plan_candidate_v1(candidate)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = (
        filename
        or "expanded_universe_per_ticker_identity_authority_plan_candidate_v1.json"
    )
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise ExpandedUniversePerTickerIdentityAuthorityPlanCandidateError(
            "expanded universe identity authority plan filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise ExpandedUniversePerTickerIdentityAuthorityPlanCandidateError(
            "expanded universe identity authority plan output already exists"
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
