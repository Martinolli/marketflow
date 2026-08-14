"""Offline operator review package for the research registry candidate."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import research_registry_candidate_service as candidate_service


ARTIFACT_KIND_RESEARCH_REGISTRY_CANDIDATE_REVIEW_PACKAGE = (
    "RESEARCH_REGISTRY_CANDIDATE_REVIEW_PACKAGE"
)
SCHEMA_VERSION_RESEARCH_REGISTRY_CANDIDATE_REVIEW_V1 = (
    "research_registry_candidate_review_v1"
)
RESEARCH_REGISTRY_CANDIDATE_REVIEW_PACKAGE_READY = (
    "RESEARCH_REGISTRY_CANDIDATE_REVIEW_PACKAGE_READY"
)
RESEARCH_REGISTRY_CANDIDATE_STATUS_BINDING = (
    "RESEARCH_REGISTRY_CANDIDATE_STATUS_BINDING"
)
RESEARCH_REGISTRY_CANDIDATE_OBJECT_BINDING = (
    "RESEARCH_REGISTRY_CANDIDATE_OBJECT_BINDING"
)
READY_FOR_OPERATOR_ASSESSMENT = "READY_FOR_OPERATOR_ASSESSMENT"

EXPECTED_REVIEWED_RESEARCH_REGISTRY_CANDIDATE_DIGEST = (
    "e62cbf4ccfbf6377f64c92ed39d1c300188f0b9923e7f8da74827db2149b7865"
)
EXPECTED_REVIEWED_CANDIDATE_CHECKLIST_TOTAL = 47
EXPECTED_REVIEWED_CANDIDATE_CHECKLIST_PASSED = 47
EXPECTED_REVIEWED_CANDIDATE_CHECKLIST_FAILED = 0
EXPECTED_REVIEWED_CANDIDATE_BLOCKER_COUNT = 0

TARGET_UNIVERSE = list(candidate_service.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(candidate_service.EXPECTED_RECORD_COUNTS)
REGISTRY_CANDIDATE_METADATA = deepcopy(candidate_service.REGISTRY_CANDIDATE_METADATA)
REGISTRY_PLANNING_DIMENSIONS = list(candidate_service.REGISTRY_PLANNING_DIMENSIONS)
FUTURE_REGISTRY_CHAIN = list(candidate_service.FUTURE_REGISTRY_CHAIN)
FUTURE_GATES = list(candidate_service.FUTURE_GATES)
RISK_CONTROLS = list(candidate_service.RISK_CONTROLS)
PLANNED_OUTPUT_NAMES = list(candidate_service.PLANNED_OUTPUT_NAMES)
PASS = candidate_service.PASS
FAIL = candidate_service.FAIL
BLOCKER = candidate_service.BLOCKER
NOT_ACCEPTED = candidate_service.NOT_ACCEPTED
NOT_AUTHORIZED = candidate_service.NOT_AUTHORIZED

REQUIRED_CHECK_IDS = [
    "candidate_kind_matches",
    "candidate_status_ready_for_review",
    "candidate_digest_matches_expected",
    "candidate_checklist_zero_blockers",
    "canonical_dataset_freeze_digest_bound",
    "canonical_dataset_results_review_digest_bound",
    "canonical_dataset_generation_digest_bound",
    "records_digest_bound",
    "identity_freeze_digest_bound",
    "target_universe_count_12",
    "target_universe_matches_candidate_universe",
    "canonical_dataset_generated_true",
    "canonical_dataset_frozen_true",
    "ready_for_research_registry_candidate_true",
    "research_registry_candidate_created_true",
    "research_registry_candidate_review_created_true",
    "research_registry_candidate_scope_candidate_only",
    "research_registry_authority_status_not_approved",
    "registry_approval_created_false",
    "research_registry_approved_false",
    "total_canonical_record_count_11946",
    "meta_record_count_913_preserved",
    "non_meta_record_counts_1003_preserved",
    "registry_metadata_reviewed",
    "registry_planning_dimensions_reviewed",
    "future_registry_chain_reviewed",
    "future_gates_defined",
    "risk_controls_defined",
    "planned_outputs_6",
    "planned_outputs_not_generated",
    "planned_outputs_research_only",
    "provider_requests_made_in_review_false",
    "live_provider_transport_enabled_in_review_false",
    "market_data_acquisition_performed_in_review_false",
    "dataset_generation_performed_in_review_false",
    "canonical_dataset_regenerated_in_review_false",
    "raw_provider_payloads_not_committed",
    "api_keys_not_stored_or_printed",
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


class ResearchRegistryCandidateReviewPackageError(ValueError):
    """Raised when the research registry candidate review package is invalid."""


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
        "message": message or (
            f"{check_id} passed" if status == PASS else f"{check_id} failed"
        ),
    }


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise ResearchRegistryCandidateReviewPackageError(f"{field} mismatch")


def _expect_true(actual: Any, field: str) -> None:
    if actual is not True:
        raise ResearchRegistryCandidateReviewPackageError(f"{field} must be true")


def _expect_false(actual: Any, field: str) -> None:
    if actual is not False:
        raise ResearchRegistryCandidateReviewPackageError(f"{field} must be false")


def _expect_digest(actual: Any, field: str) -> None:
    if not isinstance(actual, str) or len(actual) != 64:
        raise ResearchRegistryCandidateReviewPackageError(f"{field} missing")


def _candidate_for_binding(
    candidate: dict[str, Any] | None,
) -> tuple[dict[str, Any], str]:
    if candidate is None:
        source = candidate_service.build_research_registry_candidate_v1()
        binding_mode = RESEARCH_REGISTRY_CANDIDATE_STATUS_BINDING
    else:
        source = deepcopy(candidate)
        binding_mode = RESEARCH_REGISTRY_CANDIDATE_OBJECT_BINDING
    try:
        validation = candidate_service.validate_research_registry_candidate_v1(source)
    except candidate_service.ResearchRegistryCandidateError as exc:
        raise ResearchRegistryCandidateReviewPackageError(
            "research registry candidate invalid"
        ) from exc
    _expect(
        validation["research_registry_candidate_digest"],
        EXPECTED_REVIEWED_RESEARCH_REGISTRY_CANDIDATE_DIGEST,
        "reviewed candidate digest",
    )
    _expect(validation["total_checks"], EXPECTED_REVIEWED_CANDIDATE_CHECKLIST_TOTAL, "candidate checks")
    _expect(validation["passed_checks"], EXPECTED_REVIEWED_CANDIDATE_CHECKLIST_PASSED, "candidate passed checks")
    _expect(validation["failed_checks"], EXPECTED_REVIEWED_CANDIDATE_CHECKLIST_FAILED, "candidate failed checks")
    _expect(validation["blocker_count"], EXPECTED_REVIEWED_CANDIDATE_BLOCKER_COUNT, "candidate blockers")
    return source, binding_mode


def per_ticker_research_registry_review_digest_v1(entry: dict[str, Any]) -> str:
    payload = deepcopy(entry)
    payload.pop("per_ticker_research_registry_review_digest", None)
    return semantic_digest(payload)


def _per_ticker_review_entries(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for source in candidate["per_ticker_research_registry_candidates"]:
        entry = deepcopy(source)
        entry["research_registry_candidate_review_status"] = READY_FOR_OPERATOR_ASSESSMENT
        entry["research_registry_approved"] = False
        entry["source_research_registry_candidate_digest"] = candidate[
            "research_registry_candidate_digest"
        ]
        entry["per_ticker_research_registry_review_digest"] = (
            per_ticker_research_registry_review_digest_v1(entry)
        )
        result.append(entry)
    return result


def _base_review_package(candidate: dict[str, Any], binding_mode: str) -> dict[str, Any]:
    summary = candidate["candidate_summary"]
    return {
        "artifact_kind": ARTIFACT_KIND_RESEARCH_REGISTRY_CANDIDATE_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_RESEARCH_REGISTRY_CANDIDATE_REVIEW_V1,
        "review_status": RESEARCH_REGISTRY_CANDIDATE_REVIEW_PACKAGE_READY,
        "research_registry_candidate_binding_mode": binding_mode,
        "created_offline": True,
        "provider_requests_made_in_review": False,
        "live_provider_transport_enabled_in_review": False,
        "market_data_acquisition_performed_in_review": False,
        "dataset_generation_performed_in_review": False,
        "canonical_dataset_regenerated_in_review": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "research_registry_candidate_created": True,
        "research_registry_candidate_review_created": True,
        "research_registry_candidate_ready_for_operator_review": True,
        "research_registry_approved": False,
        "registry_approval_created": False,
        "canonical_dataset_generated": True,
        "canonical_dataset_frozen": True,
        "canonical_dataset_freeze_scope": candidate["canonical_dataset_freeze_scope"],
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
        "corporate_action_authority_scope": candidate["corporate_action_authority_scope"],
        "split_event_authority_created": True,
        "split_event_authority_frozen": True,
        "split_event_authority_scope": candidate["split_event_authority_scope"],
        "dividend_event_authority_created": True,
        "dividend_event_authority_frozen": True,
        "dividend_event_authority_scope": candidate["dividend_event_authority_scope"],
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
        "reviewed_research_registry_candidate_kind": candidate["artifact_kind"],
        "reviewed_research_registry_candidate_status": candidate["candidate_status"],
        "reviewed_research_registry_candidate_digest": candidate[
            "research_registry_candidate_digest"
        ],
        "reviewed_research_registry_candidate_checklist_total": summary["total_checks"],
        "reviewed_research_registry_candidate_checklist_passed": summary["passed_checks"],
        "reviewed_research_registry_candidate_checklist_failed": summary["failed_checks"],
        "reviewed_research_registry_candidate_blocker_count": summary["blocker_count"],
        "canonical_dataset_freeze_digest": candidate["canonical_dataset_freeze_digest"],
        "canonical_dataset_results_review_package_digest": candidate[
            "canonical_dataset_results_review_package_digest"
        ],
        "canonical_dataset_generation_digest": candidate["canonical_dataset_generation_digest"],
        "canonical_dataset_generation_approval_digest": candidate[
            "canonical_dataset_generation_approval_digest"
        ],
        "canonical_dataset_chain_candidate_review_package_digest": candidate[
            "canonical_dataset_chain_candidate_review_package_digest"
        ],
        "canonical_dataset_chain_candidate_digest": candidate[
            "canonical_dataset_chain_candidate_digest"
        ],
        "acquisition_generation_freeze_digest": candidate[
            "acquisition_generation_freeze_digest"
        ],
        "acquisition_generation_approval_digest": candidate[
            "acquisition_generation_approval_digest"
        ],
        "acquisition_evidence_results_review_package_digest": candidate[
            "acquisition_evidence_results_review_package_digest"
        ],
        "acquisition_provider_evidence_execution_digest": candidate[
            "acquisition_provider_evidence_execution_digest"
        ],
        "corporate_action_authority_approval_digest": candidate[
            "corporate_action_authority_approval_digest"
        ],
        "identity_authority_freeze_digest": candidate["identity_authority_freeze_digest"],
        "ticker_universe_selection_approval_digest": candidate[
            "ticker_universe_selection_approval_digest"
        ],
        "target_universe": list(candidate["target_universe"]),
        "target_universe_count": candidate["target_universe_count"],
        "source_profile": deepcopy(candidate["source_profile"]),
        "total_canonical_record_count": candidate["total_canonical_record_count"],
        "records_digest": candidate["records_digest"],
        "per_ticker_record_counts": deepcopy(candidate["per_ticker_record_counts"]),
        "data_quality_status": candidate["data_quality_status"],
        "research_registry_candidate_objective": candidate[
            "research_registry_candidate_objective"
        ],
        "research_registry_candidate_scope": candidate["research_registry_candidate_scope"],
        "research_registry_mode": candidate["research_registry_mode"],
        "research_registry_authority_status": candidate[
            "research_registry_authority_status"
        ],
        "registry_candidate_metadata": deepcopy(candidate["registry_candidate_metadata"]),
        "registry_planning_dimensions": list(candidate["registry_planning_dimensions"]),
        "per_ticker_research_registry_review_entries": _per_ticker_review_entries(candidate),
        "future_registry_chain": list(candidate["future_registry_chain"]),
        "future_gates": list(candidate["future_gates"]),
        "risk_controls": list(candidate["risk_controls"]),
        "planned_outputs": deepcopy(candidate["planned_outputs"]),
        "planned_output_count": len(candidate["planned_outputs"]),
        "planned_outputs_status": candidate_service.PLANNED_NOT_GENERATED,
        "planned_outputs_label": candidate_service.RESEARCH_ONLY_NON_ACTIONABLE,
        "registry_approval_artifact_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
    }


def _checklist(review_package: dict[str, Any]) -> list[dict[str, Any]]:
    counts = review_package.get("per_ticker_record_counts")
    counts = counts if isinstance(counts, dict) else {}
    planned = review_package.get("planned_outputs")
    planned = planned if isinstance(planned, list) else []
    values = {
        "candidate_kind_matches": (
            candidate_service.ARTIFACT_KIND_RESEARCH_REGISTRY_CANDIDATE,
            review_package.get("reviewed_research_registry_candidate_kind"),
        ),
        "candidate_status_ready_for_review": (
            candidate_service.RESEARCH_REGISTRY_READY_FOR_OPERATOR_REVIEW,
            review_package.get("reviewed_research_registry_candidate_status"),
        ),
        "candidate_digest_matches_expected": (
            EXPECTED_REVIEWED_RESEARCH_REGISTRY_CANDIDATE_DIGEST,
            review_package.get("reviewed_research_registry_candidate_digest"),
        ),
        "candidate_checklist_zero_blockers": (
            0,
            review_package.get("reviewed_research_registry_candidate_blocker_count"),
        ),
        "canonical_dataset_freeze_digest_bound": (
            candidate_service.EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST,
            review_package.get("canonical_dataset_freeze_digest"),
        ),
        "canonical_dataset_results_review_digest_bound": (
            candidate_service.EXPECTED_CANONICAL_DATASET_RESULTS_REVIEW_PACKAGE_DIGEST,
            review_package.get("canonical_dataset_results_review_package_digest"),
        ),
        "canonical_dataset_generation_digest_bound": (
            candidate_service.EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST,
            review_package.get("canonical_dataset_generation_digest"),
        ),
        "records_digest_bound": (
            candidate_service.EXPECTED_RECORDS_DIGEST,
            review_package.get("records_digest"),
        ),
        "identity_freeze_digest_bound": (
            candidate_service.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
            review_package.get("identity_authority_freeze_digest"),
        ),
        "target_universe_count_12": (12, review_package.get("target_universe_count")),
        "target_universe_matches_candidate_universe": (
            TARGET_UNIVERSE,
            review_package.get("target_universe"),
        ),
        "canonical_dataset_generated_true": (True, review_package.get("canonical_dataset_generated")),
        "canonical_dataset_frozen_true": (True, review_package.get("canonical_dataset_frozen")),
        "ready_for_research_registry_candidate_true": (True, review_package.get("ready_for_research_registry_candidate")),
        "research_registry_candidate_created_true": (True, review_package.get("research_registry_candidate_created")),
        "research_registry_candidate_review_created_true": (True, review_package.get("research_registry_candidate_review_created")),
        "research_registry_candidate_scope_candidate_only": (candidate_service.RESEARCH_REGISTRY_CANDIDATE_SCOPE, review_package.get("research_registry_candidate_scope")),
        "research_registry_authority_status_not_approved": (candidate_service.RESEARCH_REGISTRY_AUTHORITY_STATUS, review_package.get("research_registry_authority_status")),
        "registry_approval_created_false": (False, review_package.get("registry_approval_created")),
        "research_registry_approved_false": (False, review_package.get("research_registry_approved")),
        "total_canonical_record_count_11946": (11946, review_package.get("total_canonical_record_count")),
        "meta_record_count_913_preserved": (913, counts.get("META")),
        "non_meta_record_counts_1003_preserved": (True, bool(counts) and all(count == 1003 for ticker, count in counts.items() if ticker != "META")),
        "registry_metadata_reviewed": (REGISTRY_CANDIDATE_METADATA, review_package.get("registry_candidate_metadata")),
        "registry_planning_dimensions_reviewed": (REGISTRY_PLANNING_DIMENSIONS, review_package.get("registry_planning_dimensions")),
        "future_registry_chain_reviewed": (FUTURE_REGISTRY_CHAIN, review_package.get("future_registry_chain")),
        "future_gates_defined": (FUTURE_GATES, review_package.get("future_gates")),
        "risk_controls_defined": (RISK_CONTROLS, review_package.get("risk_controls")),
        "planned_outputs_6": (6, review_package.get("planned_output_count")),
        "planned_outputs_not_generated": (True, len(planned) == 6 and all(row.get("generation_status") == candidate_service.PLANNED_NOT_GENERATED for row in planned)),
        "planned_outputs_research_only": (True, len(planned) == 6 and all(row.get("output_label") == candidate_service.RESEARCH_ONLY_NON_ACTIONABLE for row in planned)),
        "provider_requests_made_in_review_false": (False, review_package.get("provider_requests_made_in_review")),
        "live_provider_transport_enabled_in_review_false": (False, review_package.get("live_provider_transport_enabled_in_review")),
        "market_data_acquisition_performed_in_review_false": (False, review_package.get("market_data_acquisition_performed_in_review")),
        "dataset_generation_performed_in_review_false": (False, review_package.get("dataset_generation_performed_in_review")),
        "canonical_dataset_regenerated_in_review_false": (False, review_package.get("canonical_dataset_regenerated_in_review")),
        "raw_provider_payloads_not_committed": (False, review_package.get("raw_provider_payloads_committed")),
        "api_keys_not_stored_or_printed": (False, review_package.get("api_keys_stored_or_printed")),
        "additional_predictive_evidence_execution_authorized_false": (False, review_package.get("additional_predictive_evidence_execution_authorized")),
        "additional_predictive_evidence_executed_false": (False, review_package.get("additional_predictive_evidence_executed")),
        "predictive_experiment_rerun_authorized_false": (False, review_package.get("predictive_experiment_rerun_authorized")),
        "new_strategy_scoring_performed_false": (False, review_package.get("new_strategy_scoring_performed")),
        "trade_recommendations_generated_false": (False, review_package.get("trade_recommendations_generated")),
        "predictive_usefulness_not_accepted": (NOT_ACCEPTED, review_package.get("predictive_usefulness")),
        "profitability_not_accepted": (NOT_ACCEPTED, review_package.get("profitability")),
        "runtime_migration_approved_false": (False, review_package.get("runtime_migration_approved")),
        "runtime_use_not_authorized": (NOT_AUTHORIZED, review_package.get("runtime_use")),
        "strategy_use_not_authorized": (NOT_AUTHORIZED, review_package.get("strategy_use")),
        "paper_trading_not_authorized": (NOT_AUTHORIZED, review_package.get("paper_trading")),
        "broker_execution_not_authorized": (NOT_AUTHORIZED, review_package.get("broker_execution")),
        "automatic_stitching_false": (False, review_package.get("automatic_stitching")),
        "no_registry_approval_artifact_created": (False, review_package.get("registry_approval_artifact_created")),
        "no_predictive_usefulness_acceptance_artifact_created": (False, review_package.get("predictive_usefulness_acceptance_artifact_created")),
        "no_profitability_acceptance_created": (False, review_package.get("profitability_acceptance_created")),
        "no_runtime_migration_approval_created": (False, review_package.get("runtime_migration_approval_created")),
    }
    return [_check(check_id, *values[check_id]) for check_id in REQUIRED_CHECK_IDS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [row for row in checklist if row.get("status") != PASS]
    return {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row.get("severity") == BLOCKER for row in failed),
        "ready_for_operator_assessment": not failed,
        "ready_for_research_registry_approval": False,
        "registry_approval_created": False,
        "research_registry_approved": False,
        "additional_predictive_evidence_execution_authorized": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def research_registry_candidate_review_package_digest_v1(
    review_package: dict[str, Any],
) -> str:
    payload = deepcopy(review_package)
    payload.pop("research_registry_candidate_review_package_digest", None)
    return semantic_digest(payload)


def build_research_registry_candidate_review_package_v1(
    candidate: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build review evidence only; never create registry approval or runtime authority."""
    source, binding_mode = _candidate_for_binding(candidate)
    package = _base_review_package(source, binding_mode)
    package["review_checklist"] = _checklist(package)
    package["review_summary"] = _summary(package["review_checklist"])
    package["research_registry_candidate_review_package_digest"] = (
        research_registry_candidate_review_package_digest_v1(package)
    )
    validate_research_registry_candidate_review_package_v1(package)
    return package


def _candidate_entry_projection(row: dict[str, Any]) -> dict[str, Any]:
    fields = (
        "ticker",
        "identity_authority_status",
        "corporate_action_authority_status",
        "acquisition_generation_status",
        "canonical_dataset_status",
        "research_registry_candidate_status",
        "historical_record_count",
        "meta_reduced_record_count_flag",
        "registry_approval_created",
        "predictive_usefulness",
        "profitability",
        "runtime_use",
        "strategy_use",
        "paper_trading",
        "broker_execution",
        "per_ticker_research_registry_candidate_digest",
    )
    return {field: row.get(field) for field in fields}


def _validate_per_ticker(review_package: dict[str, Any]) -> None:
    entries = review_package.get("per_ticker_research_registry_review_entries")
    if not isinstance(entries, list) or len(entries) != 12:
        raise ResearchRegistryCandidateReviewPackageError("per-ticker review entries mismatch")
    _expect([row.get("ticker") for row in entries], TARGET_UNIVERSE, "per-ticker order")
    for row in entries:
        ticker = row["ticker"]
        expected = {
            "identity_authority_status": "FROZEN",
            "corporate_action_authority_status": "APPROVED",
            "acquisition_generation_status": "FROZEN",
            "canonical_dataset_status": "FROZEN",
            "research_registry_candidate_status": candidate_service.PLANNED_READY_FOR_OPERATOR_REVIEW,
            "research_registry_candidate_review_status": READY_FOR_OPERATOR_ASSESSMENT,
            "historical_record_count": EXPECTED_RECORD_COUNTS[ticker],
            "meta_reduced_record_count_flag": ticker == "META",
            "registry_approval_created": False,
            "research_registry_approved": False,
            "predictive_usefulness": NOT_ACCEPTED,
            "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "source_research_registry_candidate_digest": EXPECTED_REVIEWED_RESEARCH_REGISTRY_CANDIDATE_DIGEST,
        }
        for field, value in expected.items():
            _expect(row.get(field), value, f"{ticker}.{field}")
        candidate_digest = row.get("per_ticker_research_registry_candidate_digest")
        _expect_digest(candidate_digest, f"{ticker}.per_ticker_research_registry_candidate_digest")
        _expect(
            candidate_digest,
            candidate_service.per_ticker_research_registry_candidate_digest_v1(
                _candidate_entry_projection(row)
            ),
            f"{ticker}.candidate digest",
        )
        review_digest = row.get("per_ticker_research_registry_review_digest")
        _expect_digest(review_digest, f"{ticker}.per_ticker_research_registry_review_digest")
        _expect(
            review_digest,
            per_ticker_research_registry_review_digest_v1(row),
            f"{ticker}.review digest",
        )


def validate_research_registry_candidate_review_package_v1(
    review_package: dict[str, Any],
) -> dict[str, Any]:
    """Fail closed on source drift, review drift, or downstream authority changes."""
    if not isinstance(review_package, dict):
        raise ResearchRegistryCandidateReviewPackageError("review package must be an object")
    expected = {
        "artifact_kind": ARTIFACT_KIND_RESEARCH_REGISTRY_CANDIDATE_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_RESEARCH_REGISTRY_CANDIDATE_REVIEW_V1,
        "review_status": RESEARCH_REGISTRY_CANDIDATE_REVIEW_PACKAGE_READY,
        "reviewed_research_registry_candidate_kind": candidate_service.ARTIFACT_KIND_RESEARCH_REGISTRY_CANDIDATE,
        "reviewed_research_registry_candidate_status": candidate_service.RESEARCH_REGISTRY_READY_FOR_OPERATOR_REVIEW,
        "reviewed_research_registry_candidate_digest": EXPECTED_REVIEWED_RESEARCH_REGISTRY_CANDIDATE_DIGEST,
        "reviewed_research_registry_candidate_checklist_total": EXPECTED_REVIEWED_CANDIDATE_CHECKLIST_TOTAL,
        "reviewed_research_registry_candidate_checklist_passed": EXPECTED_REVIEWED_CANDIDATE_CHECKLIST_PASSED,
        "reviewed_research_registry_candidate_checklist_failed": EXPECTED_REVIEWED_CANDIDATE_CHECKLIST_FAILED,
        "reviewed_research_registry_candidate_blocker_count": EXPECTED_REVIEWED_CANDIDATE_BLOCKER_COUNT,
        "canonical_dataset_freeze_digest": candidate_service.EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST,
        "canonical_dataset_results_review_package_digest": candidate_service.EXPECTED_CANONICAL_DATASET_RESULTS_REVIEW_PACKAGE_DIGEST,
        "canonical_dataset_generation_digest": candidate_service.EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST,
        "canonical_dataset_generation_approval_digest": candidate_service.EXPECTED_CANONICAL_DATASET_GENERATION_APPROVAL_DIGEST,
        "canonical_dataset_chain_candidate_review_package_digest": candidate_service.EXPECTED_CANONICAL_DATASET_CHAIN_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "canonical_dataset_chain_candidate_digest": candidate_service.EXPECTED_CANONICAL_DATASET_CHAIN_CANDIDATE_DIGEST,
        "acquisition_generation_freeze_digest": candidate_service.EXPECTED_ACQUISITION_GENERATION_FREEZE_DIGEST,
        "acquisition_generation_approval_digest": candidate_service.EXPECTED_ACQUISITION_GENERATION_APPROVAL_DIGEST,
        "acquisition_evidence_results_review_package_digest": candidate_service.EXPECTED_ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        "acquisition_provider_evidence_execution_digest": candidate_service.EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "corporate_action_authority_approval_digest": candidate_service.EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST,
        "identity_authority_freeze_digest": candidate_service.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
        "ticker_universe_selection_approval_digest": candidate_service.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST,
        "canonical_dataset_freeze_scope": candidate_service.freeze.CANONICAL_DATASET_FREEZE_ONLY,
        "target_universe": TARGET_UNIVERSE,
        "target_universe_count": 12,
        "source_profile": candidate_service.SOURCE_PROFILE,
        "total_canonical_record_count": 11946,
        "records_digest": candidate_service.EXPECTED_RECORDS_DIGEST,
        "per_ticker_record_counts": EXPECTED_RECORD_COUNTS,
        "data_quality_status": "PASS_WITH_PRESERVED_SOURCE_LIMITATION",
        "research_registry_candidate_objective": candidate_service.RESEARCH_REGISTRY_CANDIDATE_OBJECTIVE,
        "research_registry_candidate_scope": candidate_service.RESEARCH_REGISTRY_CANDIDATE_SCOPE,
        "research_registry_mode": candidate_service.RESEARCH_REGISTRY_MODE,
        "research_registry_authority_status": candidate_service.RESEARCH_REGISTRY_AUTHORITY_STATUS,
        "registry_candidate_metadata": REGISTRY_CANDIDATE_METADATA,
        "registry_planning_dimensions": REGISTRY_PLANNING_DIMENSIONS,
        "future_registry_chain": FUTURE_REGISTRY_CHAIN,
        "future_gates": FUTURE_GATES,
        "risk_controls": RISK_CONTROLS,
        "planned_output_count": 6,
        "planned_outputs_status": candidate_service.PLANNED_NOT_GENERATED,
        "planned_outputs_label": candidate_service.RESEARCH_ONLY_NON_ACTIONABLE,
        "corporate_action_authority_scope": "CORPORATE_ACTION_AUTHORITY_ONLY",
        "split_event_authority_scope": "SPLIT_EVENT_AUTHORITY_ONLY",
        "dividend_event_authority_scope": "DIVIDEND_EVENT_AUTHORITY_ONLY",
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
    }
    for field, value in expected.items():
        _expect(review_package.get(field), value, field)
    if review_package.get("research_registry_candidate_binding_mode") not in {
        RESEARCH_REGISTRY_CANDIDATE_STATUS_BINDING,
        RESEARCH_REGISTRY_CANDIDATE_OBJECT_BINDING,
    }:
        raise ResearchRegistryCandidateReviewPackageError(
            "research_registry_candidate_binding_mode mismatch"
        )
    for field in (
        "created_offline",
        "research_registry_candidate_created",
        "research_registry_candidate_review_created",
        "research_registry_candidate_ready_for_operator_review",
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
        "operator_review_required",
    ):
        _expect_true(review_package.get(field), field)
    for field in (
        "provider_requests_made_in_review",
        "live_provider_transport_enabled_in_review",
        "market_data_acquisition_performed_in_review",
        "dataset_generation_performed_in_review",
        "canonical_dataset_regenerated_in_review",
        "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
        "research_registry_approved",
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
        "registry_approval_artifact_created",
        "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_created",
        "runtime_migration_approval_created",
    ):
        _expect_false(review_package.get(field), field)
    planned = review_package.get("planned_outputs")
    if not isinstance(planned, list) or len(planned) != 6:
        raise ResearchRegistryCandidateReviewPackageError("planned_outputs mismatch")
    _expect([row.get("planned_output") for row in planned], PLANNED_OUTPUT_NAMES, "planned output names")
    for row in planned:
        _expect(row.get("generation_status"), candidate_service.PLANNED_NOT_GENERATED, "planned output status")
        _expect(row.get("output_label"), candidate_service.RESEARCH_ONLY_NON_ACTIONABLE, "planned output label")
    _validate_per_ticker(review_package)
    checklist = review_package.get("review_checklist")
    if not isinstance(checklist, list):
        raise ResearchRegistryCandidateReviewPackageError("review_checklist missing")
    _expect([row.get("check_id") for row in checklist], REQUIRED_CHECK_IDS, "review checklist ids")
    _expect(checklist, _checklist(review_package), "review checklist")
    if any(row.get("status") != PASS or row.get("severity") != BLOCKER for row in checklist):
        raise ResearchRegistryCandidateReviewPackageError("review checklist must pass")
    _expect(review_package.get("review_summary"), _summary(checklist), "review_summary")
    digest = review_package.get("research_registry_candidate_review_package_digest")
    _expect_digest(digest, "research_registry_candidate_review_package_digest")
    _expect(
        digest,
        research_registry_candidate_review_package_digest_v1(review_package),
        "research_registry_candidate_review_package_digest",
    )
    summary = review_package["review_summary"]
    return {
        "status": RESEARCH_REGISTRY_CANDIDATE_REVIEW_PACKAGE_READY,
        "research_registry_candidate_review_package_digest": digest,
        "total_checks": summary["total_checks"],
        "passed_checks": summary["passed_checks"],
        "failed_checks": summary["failed_checks"],
        "blocker_count": summary["blocker_count"],
        "ready_for_operator_assessment": summary["ready_for_operator_assessment"],
        "ready_for_research_registry_approval": False,
    }


def build_research_registry_candidate_review_markdown_v1(
    review_package: dict[str, Any],
) -> str:
    """Render the review package and its explicit non-approval boundaries."""
    validation = validate_research_registry_candidate_review_package_v1(review_package)
    sections = [
        ("Research Registry Candidate Review Package", [f"Artifact/status: `{review_package['artifact_kind']}` / `{validation['status']}`.", f"Review digest: `{validation['research_registry_candidate_review_package_digest']}`."]),
        ("Reviewed Candidate", [f"Candidate digest: `{review_package['reviewed_research_registry_candidate_digest']}`; checks/blockers: `{review_package['reviewed_research_registry_candidate_checklist_passed']} / {review_package['reviewed_research_registry_candidate_blocker_count']}`."]),
        ("Source Frozen Canonical Dataset", [f"Freeze/review/generation digests: `{review_package['canonical_dataset_freeze_digest']}` / `{review_package['canonical_dataset_results_review_package_digest']}` / `{review_package['canonical_dataset_generation_digest']}`."]),
        ("Target Universe", [", ".join(f"`{ticker}`" for ticker in review_package["target_universe"]) + "."]),
        ("Registry Candidate Metadata", [f"`{key}`: `{value}`." for key, value in review_package["registry_candidate_metadata"].items()]),
        ("Per-Ticker Registry Review Entries", [f"`{row['ticker']}`: `{row['research_registry_candidate_review_status']}`, `{row['historical_record_count']}` records." for row in review_package["per_ticker_research_registry_review_entries"]]),
        ("Future Registry Chain", [f"`{item}`" for item in review_package["future_registry_chain"]]),
        ("Future Gates", [f"`{item}`" for item in review_package["future_gates"]]),
        ("Risk Controls", [f"`{item}`" for item in review_package["risk_controls"]]),
        ("Registry Approval Boundary", ["This review package creates no registry approval or approval artifact."]),
        ("Predictive/Profitability Boundary", ["Predictive usefulness and profitability remain not accepted."]),
        ("Runtime Boundary", ["Runtime, strategy, paper trading, and broker execution remain `NOT_AUTHORIZED`."]),
        ("Checklist Summary", [f"Total/passed/failed/blockers: `{validation['total_checks']} / {validation['passed_checks']} / {validation['failed_checks']} / {validation['blocker_count']}`."]),
        ("Guardrails", ["No provider request, acquisition, dataset regeneration, registry approval, predictive acceptance, runtime activation, or trading action occurred."]),
    ]
    lines = ["# MarketFlow Research Registry Candidate Operator Review Package v1", "", "## Title", "", "- Research Registry Candidate Operator Review Package v1.", ""]
    for title, body in sections:
        lines.extend([f"## {title}", "", *[f"- {item}" for item in body], ""])
    return "\n".join(lines)


def write_research_registry_candidate_review_package_v1(
    output_dir: str | Path,
    *,
    candidate: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Write canonical review JSON without overwriting an existing artifact."""
    review_package = build_research_registry_candidate_review_package_v1(candidate)
    validation = validate_research_registry_candidate_review_package_v1(review_package)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "research_registry_candidate_review_package_v1.json"
    if path.exists():
        raise ResearchRegistryCandidateReviewPackageError(
            "research registry candidate review output already exists"
        )
    payload = canonical_json_bytes(review_package)
    path.write_bytes(payload)
    return {
        "path": str(path),
        "artifact_kind": review_package["artifact_kind"],
        "review_status": review_package["review_status"],
        "research_registry_candidate_review_package_digest": validation[
            "research_registry_candidate_review_package_digest"
        ],
        "payload_sha256": sha256_bytes(payload),
    }
