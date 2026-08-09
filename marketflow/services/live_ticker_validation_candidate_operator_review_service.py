"""Offline operator review package for the live ticker validation candidate."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import live_ticker_validation_candidate_service as candidate_service


ARTIFACT_KIND_LIVE_TICKER_VALIDATION_CANDIDATE_REVIEW_PACKAGE = (
    "LIVE_TICKER_VALIDATION_CANDIDATE_REVIEW_PACKAGE"
)
SCHEMA_VERSION_LIVE_TICKER_VALIDATION_CANDIDATE_REVIEW_V1 = (
    "live_ticker_validation_candidate_review_v1"
)
LIVE_TICKER_VALIDATION_CANDIDATE_REVIEW_PACKAGE_READY = (
    "LIVE_TICKER_VALIDATION_CANDIDATE_REVIEW_PACKAGE_READY"
)
LIVE_TICKER_VALIDATION_CANDIDATE_STATUS_BINDING = (
    "LIVE_TICKER_VALIDATION_CANDIDATE_STATUS_BINDING"
)
LIVE_TICKER_VALIDATION_CANDIDATE_OBJECT_BINDING = (
    "LIVE_TICKER_VALIDATION_CANDIDATE_OBJECT_BINDING"
)

EXPECTED_LIVE_TICKER_VALIDATION_CANDIDATE_DIGEST = (
    "7d4bd0b944cce2fd6be6e242683befba3ea432ddfec079eeac129722942587e7"
)
EXPECTED_REVIEWED_LIVE_TICKER_VALIDATION_CANDIDATE_CHECKLIST_TOTAL = 64
EXPECTED_REVIEWED_LIVE_TICKER_VALIDATION_CANDIDATE_CHECKLIST_PASSED = 64
EXPECTED_REVIEWED_LIVE_TICKER_VALIDATION_CANDIDATE_CHECKLIST_FAILED = 0
EXPECTED_REVIEWED_LIVE_TICKER_VALIDATION_CANDIDATE_BLOCKER_COUNT = 0

APPROVED_FOR_FUTURE_VALIDATION_ONLY = candidate_service.APPROVED_FOR_FUTURE_VALIDATION_ONLY
PLANNED_REQUIRES_SEPARATE_APPROVAL = candidate_service.PLANNED_REQUIRES_SEPARATE_APPROVAL
READ_ONLY_VALIDATION_REQUESTS_ONLY = candidate_service.READ_ONLY_VALIDATION_REQUESTS_ONLY
DO_NOT_STORE_KEYS_OR_PRINT_KEYS = candidate_service.DO_NOT_STORE_KEYS_OR_PRINT_KEYS
DO_NOT_COMMIT_RAW_PROVIDER_PAYLOADS = candidate_service.DO_NOT_COMMIT_RAW_PROVIDER_PAYLOADS
RESPECT_PROVIDER_LIMITS_AND_FAIL_CLOSED = candidate_service.RESPECT_PROVIDER_LIMITS_AND_FAIL_CLOSED
VALIDATION_RESULTS_ONLY_NOT_ACQUISITION_AUTHORITY = (
    candidate_service.VALIDATION_RESULTS_ONLY_NOT_ACQUISITION_AUTHORITY
)
NOT_REQUESTED = candidate_service.NOT_REQUESTED
NOT_PERFORMED = candidate_service.NOT_PERFORMED
NOT_VERIFIED = candidate_service.NOT_VERIFIED
NOT_CREATED = candidate_service.NOT_CREATED
NOT_AUTHORIZED = candidate_service.NOT_AUTHORIZED
PLANNED_NOT_GENERATED = candidate_service.PLANNED_NOT_GENERATED
RESEARCH_ONLY_NON_ACTIONABLE = candidate_service.RESEARCH_ONLY_NON_ACTIONABLE
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST = (
    candidate_service.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST
)
EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_SCOPE = (
    candidate_service.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_SCOPE
)
EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_DIGEST = (
    candidate_service.EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_DIGEST
)
EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    candidate_service.EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_REVIEW_PACKAGE_DIGEST
)
EXPECTED_SCOPE_EXPANSION_REVIEW_PACKAGE_DIGEST = (
    candidate_service.EXPECTED_SCOPE_EXPANSION_REVIEW_PACKAGE_DIGEST
)
EXPECTED_SCOPE_EXPANSION_CANDIDATE_DIGEST = (
    candidate_service.EXPECTED_SCOPE_EXPANSION_CANDIDATE_DIGEST
)
EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_REVIEW_PACKAGE_DIGEST = (
    candidate_service.EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_REVIEW_PACKAGE_DIGEST
)
EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE_DIGEST = (
    candidate_service.EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE_DIGEST
)
EXPECTED_ACCEPTANCE_READINESS_REVIEW_PACKAGE_DIGEST = (
    candidate_service.EXPECTED_ACCEPTANCE_READINESS_REVIEW_PACKAGE_DIGEST
)
EXPECTED_ACCEPTANCE_READINESS_CANDIDATE_DIGEST = (
    candidate_service.EXPECTED_ACCEPTANCE_READINESS_CANDIDATE_DIGEST
)

APPROVED_EXPANDED_TICKER_UNIVERSE = list(candidate_service.APPROVED_EXPANDED_TICKER_UNIVERSE)
PLANNED_VALIDATION_CHECKS = list(candidate_service.PLANNED_VALIDATION_CHECKS)
PLANNED_OUTPUT_IDS = list(candidate_service.PLANNED_OUTPUT_IDS)
FUTURE_GATES = list(candidate_service.FUTURE_GATES)
RISK_CONTROLS = list(candidate_service.RISK_CONTROLS)

REQUIRED_CHECK_IDS = [
    "live_ticker_validation_candidate_kind_matches",
    "live_ticker_validation_candidate_status_ready_for_review",
    "live_ticker_validation_candidate_digest_matches",
    "live_ticker_validation_candidate_checklist_zero_blockers",
    "ticker_universe_selection_approval_digest_bound",
    "ticker_universe_selection_candidate_digest_bound",
    "ticker_universe_selection_review_digest_bound",
    "scope_expansion_review_digest_bound",
    "approved_ticker_count_12",
    "validation_target_entries_12",
    "validation_targets_match_approved_universe",
    "validation_targets_status_future_validation_only",
    "provider_requests_made_in_review_false",
    "provider_request_authorized_false",
    "live_provider_transport_enabled_false",
    "live_ticker_validation_authorized_false",
    "live_ticker_validation_performed_false",
    "validation_targets_not_requested",
    "validation_targets_listing_not_verified",
    "validation_targets_security_type_not_verified",
    "validation_targets_exchange_not_verified",
    "validation_targets_active_status_not_verified",
    "validation_targets_authority_not_created",
    "validation_targets_runtime_not_authorized",
    "planned_validation_checks_11",
    "provider_request_policy_requires_separate_approval",
    "provider_request_policy_read_only_validation_only",
    "api_key_handling_no_store_no_print",
    "raw_payload_policy_no_commit",
    "planned_outputs_6",
    "planned_outputs_not_generated",
    "planned_outputs_research_only",
    "future_gates_10",
    "risk_controls_14",
    "new_ticker_authority_created_false",
    "new_ticker_acquisition_authorized_false",
    "dataset_generation_authorized_false",
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
    "no_live_ticker_validation_approval_artifact_created",
    "no_live_ticker_validation_artifact_created",
    "no_live_validation_results_created",
    "no_new_ticker_authority_artifact_created",
    "no_acquisition_authorization_created",
    "no_dataset_generation_authorization_created",
    "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created",
    "no_runtime_migration_approval_created",
]


class LiveTickerValidationCandidateReviewPackageError(ValueError):
    """Raised when the live ticker validation candidate review package is invalid."""


def _check(
    check_id: str,
    expected: Any,
    actual: Any,
    *,
    severity: str = BLOCKER,
) -> dict[str, Any]:
    status = PASS if actual == expected else FAIL
    return {
        "check_id": check_id,
        "status": status,
        "expected": expected,
        "actual": actual,
        "severity": severity,
        "message": f"{check_id} passed" if status == PASS else f"{check_id} failed",
    }


def _expect(actual: Any, expected: Any, field_name: str) -> None:
    if actual != expected:
        raise LiveTickerValidationCandidateReviewPackageError(f"{field_name} mismatch")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise LiveTickerValidationCandidateReviewPackageError(f"{field_name} must be true")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise LiveTickerValidationCandidateReviewPackageError(f"{field_name} must be false")


def _path_text(path: Path) -> str:
    return str(path).replace("\\", "/")


def _recorded_live_ticker_validation_candidate() -> dict[str, Any]:
    tickers = list(APPROVED_EXPANDED_TICKER_UNIVERSE)
    return {
        "artifact_kind": candidate_service.ARTIFACT_KIND_LIVE_TICKER_VALIDATION_CANDIDATE,
        "candidate_status": candidate_service.LIVE_TICKER_VALIDATION_READY_FOR_OPERATOR_REVIEW,
        "live_ticker_validation_candidate_digest": EXPECTED_LIVE_TICKER_VALIDATION_CANDIDATE_DIGEST,
        "validation_summary": {
            "total_checks": EXPECTED_REVIEWED_LIVE_TICKER_VALIDATION_CANDIDATE_CHECKLIST_TOTAL,
            "passed_checks": EXPECTED_REVIEWED_LIVE_TICKER_VALIDATION_CANDIDATE_CHECKLIST_PASSED,
            "failed_checks": EXPECTED_REVIEWED_LIVE_TICKER_VALIDATION_CANDIDATE_CHECKLIST_FAILED,
            "blocker_count": EXPECTED_REVIEWED_LIVE_TICKER_VALIDATION_CANDIDATE_BLOCKER_COUNT,
        },
        "ticker_universe_selection_approval_digest": (
            EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST
        ),
        "ticker_universe_selection_approval_scope": (
            EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_SCOPE
        ),
        "ticker_universe_selection_candidate_digest": (
            EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_DIGEST
        ),
        "ticker_universe_selection_candidate_review_package_digest": (
            EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "predictive_evidence_scope_expansion_plan_candidate_review_package_digest": (
            EXPECTED_SCOPE_EXPANSION_REVIEW_PACKAGE_DIGEST
        ),
        "predictive_evidence_scope_expansion_plan_candidate_digest": (
            EXPECTED_SCOPE_EXPANSION_CANDIDATE_DIGEST
        ),
        "additional_predictive_evidence_plan_candidate_review_package_digest": (
            EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_REVIEW_PACKAGE_DIGEST
        ),
        "additional_predictive_evidence_plan_candidate_digest": (
            EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE_DIGEST
        ),
        "predictive_usefulness_acceptance_readiness_candidate_review_package_digest": (
            EXPECTED_ACCEPTANCE_READINESS_REVIEW_PACKAGE_DIGEST
        ),
        "predictive_usefulness_acceptance_readiness_candidate_digest": (
            EXPECTED_ACCEPTANCE_READINESS_CANDIDATE_DIGEST
        ),
        "approved_expanded_ticker_universe": tickers,
        "approved_expanded_ticker_count": len(tickers),
        "validation_target_entries": candidate_service._validation_target_entries(tickers),
        "validation_target_count": len(tickers),
        "planned_validation_checks": candidate_service._planned_validation_checks(),
        "planned_validation_check_count": len(PLANNED_VALIDATION_CHECKS),
        "provider_request_policy": candidate_service._provider_request_policy(),
        "planned_outputs": candidate_service._planned_outputs(),
        "planned_output_count": len(PLANNED_OUTPUT_IDS),
        "future_gates": list(FUTURE_GATES),
        "future_gate_count": len(FUTURE_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "risk_control_count": len(RISK_CONTROLS),
    }


def _candidate_for_binding(candidate: dict[str, Any] | None) -> tuple[dict[str, Any], str]:
    if candidate is None:
        return (
            _recorded_live_ticker_validation_candidate(),
            LIVE_TICKER_VALIDATION_CANDIDATE_STATUS_BINDING,
        )
    candidate_service.validate_live_ticker_validation_candidate_v1(candidate)
    return deepcopy(candidate), LIVE_TICKER_VALIDATION_CANDIDATE_OBJECT_BINDING


def _base_review_package(candidate: dict[str, Any], binding_mode: str) -> dict[str, Any]:
    summary = candidate["validation_summary"]
    return {
        "artifact_kind": ARTIFACT_KIND_LIVE_TICKER_VALIDATION_CANDIDATE_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_LIVE_TICKER_VALIDATION_CANDIDATE_REVIEW_V1,
        "review_status": LIVE_TICKER_VALIDATION_CANDIDATE_REVIEW_PACKAGE_READY,
        "live_ticker_validation_candidate_binding_mode": binding_mode,
        "operator_decision_required": True,
        "operator_decision": None,
        "created_offline": True,
        "provider_requests_made_in_review": False,
        "provider_request_authorized": False,
        "live_provider_transport_enabled": False,
        "live_ticker_validation_candidate_created": True,
        "live_ticker_validation_authorized": False,
        "live_ticker_validation_performed": False,
        "ticker_universe_selection_approved": True,
        "expanded_ticker_universe_approved": True,
        "new_ticker_authority_created": False,
        "new_ticker_acquisition_authorized": False,
        "dataset_generation_authorized": False,
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
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "automatic_stitching": False,
        "ready_for_live_ticker_validation_approval": False,
        "live_ticker_validation_approval_artifact_created": False,
        "live_ticker_validation_artifact_created": False,
        "live_validation_results_created": False,
        "new_ticker_authority_artifact_created": False,
        "acquisition_authorization_artifact_created": False,
        "dataset_generation_authorization_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_artifact_created": False,
        "runtime_migration_approval_artifact_created": False,
        "reviewed_live_ticker_validation_candidate_kind": candidate["artifact_kind"],
        "reviewed_live_ticker_validation_candidate_status": candidate["candidate_status"],
        "reviewed_live_ticker_validation_candidate_digest": candidate[
            "live_ticker_validation_candidate_digest"
        ],
        "reviewed_live_ticker_validation_candidate_checklist_total": summary["total_checks"],
        "reviewed_live_ticker_validation_candidate_checklist_passed": summary["passed_checks"],
        "reviewed_live_ticker_validation_candidate_checklist_failed": summary["failed_checks"],
        "reviewed_live_ticker_validation_candidate_blocker_count": summary["blocker_count"],
        "ticker_universe_selection_approval_digest": candidate[
            "ticker_universe_selection_approval_digest"
        ],
        "ticker_universe_selection_approval_scope": candidate[
            "ticker_universe_selection_approval_scope"
        ],
        "ticker_universe_selection_candidate_digest": candidate[
            "ticker_universe_selection_candidate_digest"
        ],
        "ticker_universe_selection_candidate_review_package_digest": candidate[
            "ticker_universe_selection_candidate_review_package_digest"
        ],
        "predictive_evidence_scope_expansion_plan_candidate_review_package_digest": candidate[
            "predictive_evidence_scope_expansion_plan_candidate_review_package_digest"
        ],
        "predictive_evidence_scope_expansion_plan_candidate_digest": candidate[
            "predictive_evidence_scope_expansion_plan_candidate_digest"
        ],
        "additional_predictive_evidence_plan_candidate_review_package_digest": candidate[
            "additional_predictive_evidence_plan_candidate_review_package_digest"
        ],
        "additional_predictive_evidence_plan_candidate_digest": candidate[
            "additional_predictive_evidence_plan_candidate_digest"
        ],
        "predictive_usefulness_acceptance_readiness_candidate_review_package_digest": (
            candidate["predictive_usefulness_acceptance_readiness_candidate_review_package_digest"]
        ),
        "predictive_usefulness_acceptance_readiness_candidate_digest": candidate[
            "predictive_usefulness_acceptance_readiness_candidate_digest"
        ],
        "approved_expanded_ticker_universe": list(candidate["approved_expanded_ticker_universe"]),
        "approved_expanded_ticker_count": candidate["approved_expanded_ticker_count"],
        "validation_target_entries": deepcopy(candidate["validation_target_entries"]),
        "validation_target_count": candidate["validation_target_count"],
        "planned_validation_checks": deepcopy(candidate["planned_validation_checks"]),
        "planned_validation_check_count": candidate["planned_validation_check_count"],
        "provider_request_policy": deepcopy(candidate["provider_request_policy"]),
        "planned_outputs": deepcopy(candidate["planned_outputs"]),
        "planned_output_count": candidate["planned_output_count"],
        "future_gates": list(candidate["future_gates"]),
        "future_gate_count": candidate["future_gate_count"],
        "risk_controls": list(candidate["risk_controls"]),
        "risk_control_count": candidate["risk_control_count"],
    }


def _all_targets(review_package: dict[str, Any]) -> list[dict[str, Any]]:
    entries = review_package.get("validation_target_entries")
    return entries if isinstance(entries, list) else []


def _targets_have(field: str, expected: Any, review_package: dict[str, Any]) -> bool:
    targets = _all_targets(review_package)
    return bool(targets) and all(target.get(field) == expected for target in targets)


def _target_authorities_not_created(review_package: dict[str, Any]) -> bool:
    fields = (
        "identity_authority_status",
        "split_event_authority_status",
        "dividend_event_authority_status",
        "acquisition_authority_status",
        "canonical_dataset_authority_status",
        "registry_approval_status",
    )
    targets = _all_targets(review_package)
    return bool(targets) and all(
        target.get(field) == NOT_CREATED for target in targets for field in fields
    )


def _target_uses_not_authorized(review_package: dict[str, Any]) -> bool:
    fields = ("research_use_status", "runtime_use", "strategy_use", "paper_trading", "broker_execution")
    targets = _all_targets(review_package)
    return bool(targets) and all(
        target.get(field) == NOT_AUTHORIZED for target in targets for field in fields
    )


def _planned_checks_valid(review_package: dict[str, Any]) -> bool:
    checks = review_package.get("planned_validation_checks")
    expected_names = [name for name, _purpose in PLANNED_VALIDATION_CHECKS]
    if not isinstance(checks, list) or len(checks) != len(expected_names):
        return False
    return (
        [item.get("check_name") for item in checks if isinstance(item, dict)] == expected_names
        and all(item.get("planned_provider_interaction_required") is True for item in checks)
        and all(item.get("performed_now") is False for item in checks)
        and all(item.get("operator_approval_required_before_execution") is True for item in checks)
    )


def _planned_outputs_valid(review_package: dict[str, Any]) -> bool:
    outputs = review_package.get("planned_outputs")
    return (
        isinstance(outputs, list)
        and len(outputs) == len(PLANNED_OUTPUT_IDS)
        and [item.get("output_id") for item in outputs if isinstance(item, dict)] == PLANNED_OUTPUT_IDS
        and all(item.get("generation_status") == PLANNED_NOT_GENERATED for item in outputs)
        and all(item.get("actionability_label") == RESEARCH_ONLY_NON_ACTIONABLE for item in outputs)
    )


def _checklist(review_package: dict[str, Any]) -> list[dict[str, Any]]:
    targets = _all_targets(review_package)
    target_tickers = [target.get("ticker") for target in targets if isinstance(target, dict)]
    policy = review_package.get("provider_request_policy")
    policy = policy if isinstance(policy, dict) else {}
    return [
        _check("live_ticker_validation_candidate_kind_matches", candidate_service.ARTIFACT_KIND_LIVE_TICKER_VALIDATION_CANDIDATE, review_package.get("reviewed_live_ticker_validation_candidate_kind")),
        _check("live_ticker_validation_candidate_status_ready_for_review", candidate_service.LIVE_TICKER_VALIDATION_READY_FOR_OPERATOR_REVIEW, review_package.get("reviewed_live_ticker_validation_candidate_status")),
        _check("live_ticker_validation_candidate_digest_matches", EXPECTED_LIVE_TICKER_VALIDATION_CANDIDATE_DIGEST, review_package.get("reviewed_live_ticker_validation_candidate_digest")),
        _check("live_ticker_validation_candidate_checklist_zero_blockers", 0, review_package.get("reviewed_live_ticker_validation_candidate_blocker_count")),
        _check("ticker_universe_selection_approval_digest_bound", EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST, review_package.get("ticker_universe_selection_approval_digest")),
        _check("ticker_universe_selection_candidate_digest_bound", EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_DIGEST, review_package.get("ticker_universe_selection_candidate_digest")),
        _check("ticker_universe_selection_review_digest_bound", EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_REVIEW_PACKAGE_DIGEST, review_package.get("ticker_universe_selection_candidate_review_package_digest")),
        _check("scope_expansion_review_digest_bound", EXPECTED_SCOPE_EXPANSION_REVIEW_PACKAGE_DIGEST, review_package.get("predictive_evidence_scope_expansion_plan_candidate_review_package_digest")),
        _check("approved_ticker_count_12", 12, review_package.get("approved_expanded_ticker_count")),
        _check("validation_target_entries_12", 12, review_package.get("validation_target_count")),
        _check("validation_targets_match_approved_universe", APPROVED_EXPANDED_TICKER_UNIVERSE, target_tickers),
        _check("validation_targets_status_future_validation_only", True, _targets_have("validation_target_status", APPROVED_FOR_FUTURE_VALIDATION_ONLY, review_package)),
        _check("provider_requests_made_in_review_false", False, review_package.get("provider_requests_made_in_review")),
        _check("provider_request_authorized_false", False, review_package.get("provider_request_authorized")),
        _check("live_provider_transport_enabled_false", False, review_package.get("live_provider_transport_enabled")),
        _check("live_ticker_validation_authorized_false", False, review_package.get("live_ticker_validation_authorized")),
        _check("live_ticker_validation_performed_false", False, review_package.get("live_ticker_validation_performed")),
        _check("validation_targets_not_requested", True, _targets_have("provider_request_status", NOT_REQUESTED, review_package)),
        _check("validation_targets_listing_not_verified", True, _targets_have("listing_status", NOT_VERIFIED, review_package)),
        _check("validation_targets_security_type_not_verified", True, _targets_have("security_type_status", NOT_VERIFIED, review_package)),
        _check("validation_targets_exchange_not_verified", True, _targets_have("exchange_status", NOT_VERIFIED, review_package)),
        _check("validation_targets_active_status_not_verified", True, _targets_have("active_status", NOT_VERIFIED, review_package)),
        _check("validation_targets_authority_not_created", True, _target_authorities_not_created(review_package)),
        _check("validation_targets_runtime_not_authorized", True, _target_uses_not_authorized(review_package)),
        _check("planned_validation_checks_11", 11, review_package.get("planned_validation_check_count")),
        _check("provider_request_policy_requires_separate_approval", PLANNED_REQUIRES_SEPARATE_APPROVAL, policy.get("future_provider_request_policy_status")),
        _check("provider_request_policy_read_only_validation_only", READ_ONLY_VALIDATION_REQUESTS_ONLY, policy.get("allowed_future_request_type")),
        _check("api_key_handling_no_store_no_print", DO_NOT_STORE_KEYS_OR_PRINT_KEYS, policy.get("api_key_handling")),
        _check("raw_payload_policy_no_commit", DO_NOT_COMMIT_RAW_PROVIDER_PAYLOADS, policy.get("raw_payload_policy")),
        _check("planned_outputs_6", 6, review_package.get("planned_output_count")),
        _check("planned_outputs_not_generated", True, _planned_outputs_valid(review_package)),
        _check("planned_outputs_research_only", True, _planned_outputs_valid(review_package)),
        _check("future_gates_10", 10, review_package.get("future_gate_count")),
        _check("risk_controls_14", 14, review_package.get("risk_control_count")),
        _check("new_ticker_authority_created_false", False, review_package.get("new_ticker_authority_created")),
        _check("new_ticker_acquisition_authorized_false", False, review_package.get("new_ticker_acquisition_authorized")),
        _check("dataset_generation_authorized_false", False, review_package.get("dataset_generation_authorized")),
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
        _check("runtime_use_not_authorized", NOT_AUTHORIZED, review_package.get("runtime_use")),
        _check("strategy_use_not_authorized", NOT_AUTHORIZED, review_package.get("strategy_use")),
        _check("paper_trading_not_authorized", NOT_AUTHORIZED, review_package.get("paper_trading")),
        _check("broker_execution_not_authorized", NOT_AUTHORIZED, review_package.get("broker_execution")),
        _check("automatic_stitching_false", False, review_package.get("automatic_stitching")),
        _check("no_live_ticker_validation_approval_artifact_created", False, review_package.get("live_ticker_validation_approval_artifact_created")),
        _check("no_live_ticker_validation_artifact_created", False, review_package.get("live_ticker_validation_artifact_created")),
        _check("no_live_validation_results_created", False, review_package.get("live_validation_results_created")),
        _check("no_new_ticker_authority_artifact_created", False, review_package.get("new_ticker_authority_artifact_created")),
        _check("no_acquisition_authorization_created", False, review_package.get("acquisition_authorization_artifact_created")),
        _check("no_dataset_generation_authorization_created", False, review_package.get("dataset_generation_authorization_created")),
        _check("no_predictive_usefulness_acceptance_artifact_created", False, review_package.get("predictive_usefulness_acceptance_artifact_created")),
        _check("no_profitability_acceptance_created", False, review_package.get("profitability_acceptance_artifact_created")),
        _check("no_runtime_migration_approval_created", False, review_package.get("runtime_migration_approval_artifact_created")),
    ]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(checklist)
    passed = sum(1 for item in checklist if item.get("status") == PASS)
    failed = total - passed
    blocker_count = sum(
        1 for item in checklist if item.get("status") == FAIL and item.get("severity") == BLOCKER
    )
    return {
        "total_checks": total,
        "passed_checks": passed,
        "failed_checks": failed,
        "blocker_count": blocker_count,
        "ready_for_operator_assessment": failed == 0,
        "ready_for_live_ticker_validation_approval": False,
        "live_ticker_validation_authorized": False,
        "live_ticker_validation_performed": False,
        "new_ticker_authority_authorized": False,
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
    payload.pop("live_ticker_validation_candidate_review_package_digest", None)
    return payload


def live_ticker_validation_candidate_review_package_digest_v1(
    review_package: dict[str, Any],
) -> str:
    """Return the deterministic digest for the live ticker validation review package."""
    return semantic_digest(_digest_payload(review_package))


def build_live_ticker_validation_candidate_review_package_v1(
    candidate: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build an offline review package without authorizing live validation."""
    bound_candidate, binding_mode = _candidate_for_binding(candidate)
    review_package = _base_review_package(bound_candidate, binding_mode)
    review_package["review_checklist"] = _checklist(review_package)
    review_package["review_summary"] = _summary(review_package["review_checklist"])
    review_package["live_ticker_validation_candidate_review_package_digest"] = (
        live_ticker_validation_candidate_review_package_digest_v1(review_package)
    )
    validate_live_ticker_validation_candidate_review_package_v1(review_package)
    return review_package


def _reject_forbidden_values(mapping: dict[str, Any], *, path: str = "review_package") -> None:
    forbidden_artifact_values = {
        "LIVE_TICKER_VALIDATION_APPROVED",
        "LIVE_TICKER_VALIDATION_PERFORMED",
        "LIVE_TICKER_VALIDATION_RESULTS",
        "NEW_TICKER_AUTHORITY_APPROVED",
        "NEW_TICKER_ACQUISITION_AUTHORIZED",
        "ACQUISITION_GENERATION_AUTHORIZED",
        "CANONICAL_DATASET_AUTHORIZED",
        "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED",
        "PREDICTIVE_USEFULNESS_ACCEPTANCE_CANDIDATE",
        "PREDICTIVE_USEFULNESS_ACCEPTED",
        "PROFITABILITY_ACCEPTED",
        "RUNTIME_MIGRATION_APPROVED",
        "RUNTIME_MIGRATION_ACTIVE",
        "STRATEGY_RUNTIME_MIGRATION",
        "TRADE_RECOMMENDATIONS",
    }
    forbidden_true_fields = {
        "provider_requests_made",
        "provider_requests_made_in_review",
        "provider_request_authorized",
        "live_provider_transport_enabled",
        "live_ticker_validation_authorized",
        "live_ticker_validation_performed",
        "ready_for_live_ticker_validation_approval",
        "new_ticker_authority_created",
        "new_ticker_acquisition_authorized",
        "dataset_generation_authorized",
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
        "live_ticker_validation_approval_artifact_created",
        "live_ticker_validation_artifact_created",
        "live_validation_results_created",
        "new_ticker_authority_artifact_created",
        "acquisition_authorization_artifact_created",
        "dataset_generation_authorization_created",
        "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_artifact_created",
        "runtime_migration_approval_artifact_created",
    }
    for key, value in mapping.items():
        current_path = f"{path}.{key}"
        if isinstance(value, str) and value in forbidden_artifact_values:
            raise LiveTickerValidationCandidateReviewPackageError(
                f"{current_path} must not emit {value}"
            )
        if key in forbidden_true_fields and value is True:
            raise LiveTickerValidationCandidateReviewPackageError(
                f"{current_path} must be false"
            )
        if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"}:
            if value == "AUTHORIZED":
                raise LiveTickerValidationCandidateReviewPackageError(
                    f"{current_path} must not be AUTHORIZED"
                )
        if key in {"predictive_usefulness", "profitability"} and value == "accepted":
            raise LiveTickerValidationCandidateReviewPackageError(
                f"{current_path} must not be accepted"
            )
        if isinstance(value, dict):
            _reject_forbidden_values(value, path=current_path)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, dict):
                    _reject_forbidden_values(item, path=f"{current_path}[{index}]")


def _validate_validation_targets(review_package: dict[str, Any]) -> None:
    tickers = review_package.get("approved_expanded_ticker_universe")
    targets = review_package.get("validation_target_entries")
    if tickers != APPROVED_EXPANDED_TICKER_UNIVERSE:
        raise LiveTickerValidationCandidateReviewPackageError(
            "approved ticker universe mismatch"
        )
    _expect(
        review_package.get("approved_expanded_ticker_count"),
        len(APPROVED_EXPANDED_TICKER_UNIVERSE),
        "approved_expanded_ticker_count",
    )
    if not isinstance(targets, list) or len(targets) != len(APPROVED_EXPANDED_TICKER_UNIVERSE):
        raise LiveTickerValidationCandidateReviewPackageError(
            "validation_target_entries mismatch"
        )
    _expect(
        review_package.get("validation_target_count"),
        len(APPROVED_EXPANDED_TICKER_UNIVERSE),
        "validation_target_count",
    )
    if [target.get("ticker") for target in targets] != APPROVED_EXPANDED_TICKER_UNIVERSE:
        raise LiveTickerValidationCandidateReviewPackageError(
            "validation target tickers mismatch"
        )
    expected_statuses = {
        "validation_target_status": APPROVED_FOR_FUTURE_VALIDATION_ONLY,
        "live_validation_status": NOT_PERFORMED,
        "provider_request_status": NOT_REQUESTED,
        "listing_status": NOT_VERIFIED,
        "security_type_status": NOT_VERIFIED,
        "exchange_status": NOT_VERIFIED,
        "active_status": NOT_VERIFIED,
        "delisting_status": NOT_VERIFIED,
        "tradability_status": NOT_VERIFIED,
        "corporate_action_data_availability_status": NOT_VERIFIED,
        "historical_aggregate_data_availability_status": NOT_VERIFIED,
        "identity_authority_status": NOT_CREATED,
        "split_event_authority_status": NOT_CREATED,
        "dividend_event_authority_status": NOT_CREATED,
        "acquisition_authority_status": NOT_CREATED,
        "canonical_dataset_authority_status": NOT_CREATED,
        "registry_approval_status": NOT_CREATED,
        "research_use_status": NOT_AUTHORIZED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
    }
    for target in targets:
        ticker = target.get("ticker")
        for field, expected in expected_statuses.items():
            _expect(target.get(field), expected, f"validation_target_entries.{ticker}.{field}")


def _validate_planning_sections(review_package: dict[str, Any]) -> None:
    if not _planned_checks_valid(review_package):
        raise LiveTickerValidationCandidateReviewPackageError(
            "planned_validation_checks mismatch"
        )
    _expect(
        review_package.get("planned_validation_check_count"),
        len(PLANNED_VALIDATION_CHECKS),
        "planned_validation_check_count",
    )
    _expect(
        review_package.get("provider_request_policy"),
        candidate_service._provider_request_policy(),
        "provider_request_policy",
    )
    if not _planned_outputs_valid(review_package):
        raise LiveTickerValidationCandidateReviewPackageError("planned_outputs mismatch")
    _expect(review_package.get("planned_output_count"), len(PLANNED_OUTPUT_IDS), "planned_output_count")
    _expect(review_package.get("future_gates"), FUTURE_GATES, "future_gates")
    _expect(review_package.get("future_gate_count"), len(FUTURE_GATES), "future_gate_count")
    _expect(review_package.get("risk_controls"), RISK_CONTROLS, "risk_controls")
    _expect(review_package.get("risk_control_count"), len(RISK_CONTROLS), "risk_control_count")


def validate_live_ticker_validation_candidate_review_package_v1(
    review_package: dict[str, Any],
) -> dict[str, Any]:
    """Validate the review package while enforcing all non-execution boundaries."""
    if not isinstance(review_package, dict):
        raise LiveTickerValidationCandidateReviewPackageError(
            "review_package must be a JSON object"
        )
    _reject_forbidden_values(review_package)
    _expect(
        review_package.get("artifact_kind"),
        ARTIFACT_KIND_LIVE_TICKER_VALIDATION_CANDIDATE_REVIEW_PACKAGE,
        "artifact_kind",
    )
    _expect(
        review_package.get("schema_version"),
        SCHEMA_VERSION_LIVE_TICKER_VALIDATION_CANDIDATE_REVIEW_V1,
        "schema_version",
    )
    _expect(
        review_package.get("review_status"),
        LIVE_TICKER_VALIDATION_CANDIDATE_REVIEW_PACKAGE_READY,
        "review_status",
    )
    if review_package.get("live_ticker_validation_candidate_binding_mode") not in {
        LIVE_TICKER_VALIDATION_CANDIDATE_STATUS_BINDING,
        LIVE_TICKER_VALIDATION_CANDIDATE_OBJECT_BINDING,
    }:
        raise LiveTickerValidationCandidateReviewPackageError(
            "live_ticker_validation_candidate_binding_mode mismatch"
        )
    for field in (
        "operator_decision_required",
        "created_offline",
        "live_ticker_validation_candidate_created",
        "ticker_universe_selection_approved",
        "expanded_ticker_universe_approved",
        "research_only",
    ):
        _expect_true(review_package.get(field), field)
    _expect(review_package.get("operator_decision"), None, "operator_decision")
    for field in (
        "provider_requests_made_in_review",
        "provider_request_authorized",
        "live_provider_transport_enabled",
        "live_ticker_validation_authorized",
        "live_ticker_validation_performed",
        "new_ticker_authority_created",
        "new_ticker_acquisition_authorized",
        "dataset_generation_authorized",
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
        "ready_for_live_ticker_validation_approval",
        "live_ticker_validation_approval_artifact_created",
        "live_ticker_validation_artifact_created",
        "live_validation_results_created",
        "new_ticker_authority_artifact_created",
        "acquisition_authorization_artifact_created",
        "dataset_generation_authorization_created",
        "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_artifact_created",
        "runtime_migration_approval_artifact_created",
    ):
        _expect_false(review_package.get(field), field)
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(review_package.get(field), NOT_AUTHORIZED, field)
    for field, expected in {
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "reviewed_live_ticker_validation_candidate_kind": (
            candidate_service.ARTIFACT_KIND_LIVE_TICKER_VALIDATION_CANDIDATE
        ),
        "reviewed_live_ticker_validation_candidate_status": (
            candidate_service.LIVE_TICKER_VALIDATION_READY_FOR_OPERATOR_REVIEW
        ),
        "reviewed_live_ticker_validation_candidate_digest": (
            EXPECTED_LIVE_TICKER_VALIDATION_CANDIDATE_DIGEST
        ),
        "reviewed_live_ticker_validation_candidate_checklist_total": (
            EXPECTED_REVIEWED_LIVE_TICKER_VALIDATION_CANDIDATE_CHECKLIST_TOTAL
        ),
        "reviewed_live_ticker_validation_candidate_checklist_passed": (
            EXPECTED_REVIEWED_LIVE_TICKER_VALIDATION_CANDIDATE_CHECKLIST_PASSED
        ),
        "reviewed_live_ticker_validation_candidate_checklist_failed": (
            EXPECTED_REVIEWED_LIVE_TICKER_VALIDATION_CANDIDATE_CHECKLIST_FAILED
        ),
        "reviewed_live_ticker_validation_candidate_blocker_count": (
            EXPECTED_REVIEWED_LIVE_TICKER_VALIDATION_CANDIDATE_BLOCKER_COUNT
        ),
        "ticker_universe_selection_approval_digest": (
            EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST
        ),
        "ticker_universe_selection_approval_scope": (
            EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_SCOPE
        ),
        "ticker_universe_selection_candidate_digest": (
            EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_DIGEST
        ),
        "ticker_universe_selection_candidate_review_package_digest": (
            EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "predictive_evidence_scope_expansion_plan_candidate_review_package_digest": (
            EXPECTED_SCOPE_EXPANSION_REVIEW_PACKAGE_DIGEST
        ),
        "predictive_evidence_scope_expansion_plan_candidate_digest": (
            EXPECTED_SCOPE_EXPANSION_CANDIDATE_DIGEST
        ),
        "additional_predictive_evidence_plan_candidate_review_package_digest": (
            EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_REVIEW_PACKAGE_DIGEST
        ),
        "additional_predictive_evidence_plan_candidate_digest": (
            EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE_DIGEST
        ),
        "predictive_usefulness_acceptance_readiness_candidate_review_package_digest": (
            EXPECTED_ACCEPTANCE_READINESS_REVIEW_PACKAGE_DIGEST
        ),
        "predictive_usefulness_acceptance_readiness_candidate_digest": (
            EXPECTED_ACCEPTANCE_READINESS_CANDIDATE_DIGEST
        ),
    }.items():
        _expect(review_package.get(field), expected, field)
    _validate_validation_targets(review_package)
    _validate_planning_sections(review_package)
    checklist = review_package.get("review_checklist")
    if not isinstance(checklist, list):
        raise LiveTickerValidationCandidateReviewPackageError("review_checklist missing")
    expected_checklist = _checklist(review_package)
    _expect(
        [item.get("check_id") for item in checklist if isinstance(item, dict)],
        REQUIRED_CHECK_IDS,
        "review_checklist check IDs",
    )
    failed = [item for item in expected_checklist if item["status"] != PASS]
    if failed:
        raise LiveTickerValidationCandidateReviewPackageError(
            f"review checklist contains failed check: {failed[0]['check_id']}"
        )
    _expect(checklist, expected_checklist, "review_checklist")
    expected_summary = _summary(expected_checklist)
    _expect(review_package.get("review_summary"), expected_summary, "review_summary")
    digest = review_package.get("live_ticker_validation_candidate_review_package_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise LiveTickerValidationCandidateReviewPackageError(
            "live_ticker_validation_candidate_review_package_digest missing"
        )
    _expect(
        digest,
        live_ticker_validation_candidate_review_package_digest_v1(review_package),
        "live_ticker_validation_candidate_review_package_digest",
    )
    return {
        "status": "LIVE_TICKER_VALIDATION_CANDIDATE_REVIEW_PACKAGE_VALID",
        "artifact_kind": review_package["artifact_kind"],
        "review_status": review_package["review_status"],
        "live_ticker_validation_candidate_review_package_digest": digest,
        "reviewed_live_ticker_validation_candidate_digest": review_package[
            "reviewed_live_ticker_validation_candidate_digest"
        ],
        "approved_expanded_ticker_universe": list(
            review_package["approved_expanded_ticker_universe"]
        ),
        "approved_expanded_ticker_count": review_package["approved_expanded_ticker_count"],
        "validation_target_count": review_package["validation_target_count"],
        "provider_requests_made_in_review": False,
        "provider_request_authorized": False,
        "live_provider_transport_enabled": False,
        "live_ticker_validation_authorized": False,
        "live_ticker_validation_performed": False,
        "new_ticker_authority_created": False,
        "new_ticker_acquisition_authorized": False,
        "dataset_generation_authorized": False,
        "additional_predictive_evidence_execution_authorized": False,
        "additional_predictive_evidence_executed": False,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "runtime_migration_approved": False,
        "runtime_migration_active": False,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "total_checks": expected_summary["total_checks"],
        "passed_checks": expected_summary["passed_checks"],
        "failed_checks": expected_summary["failed_checks"],
        "blocker_count": expected_summary["blocker_count"],
        "ready_for_operator_assessment": expected_summary["ready_for_operator_assessment"],
        "ready_for_live_ticker_validation_approval": False,
    }


def build_live_ticker_validation_candidate_review_markdown_v1(
    review_package: dict[str, Any],
) -> str:
    """Render a sanitized live ticker validation candidate review status document."""
    validation = validate_live_ticker_validation_candidate_review_package_v1(review_package)
    summary = review_package["review_summary"]
    lines = [
        "# MarketFlow Live Ticker Validation Candidate Operator Review Package Status",
        "",
        "## Title",
        "- Live Ticker Validation Candidate Operator Review Package v1.",
        "",
        "## Purpose",
        "- Bind the live ticker validation candidate for operator assessment.",
        "- This package does not authorize provider requests or perform live validation.",
        "",
        "## Review Package",
        f"- Artifact kind: `{review_package['artifact_kind']}`",
        f"- Review status: `{review_package['review_status']}`",
        f"- Schema version: `{review_package['schema_version']}`",
        f"- Review package digest: `{validation['live_ticker_validation_candidate_review_package_digest']}`",
        f"- Candidate binding mode: `{review_package['live_ticker_validation_candidate_binding_mode']}`",
        f"- Operator decision required: `{review_package['operator_decision_required']}`",
        f"- Operator decision: `{review_package['operator_decision']}`",
        f"- Created offline: `{review_package['created_offline']}`",
        "",
        "## Reviewed Candidate Evidence",
        f"- Candidate kind: `{review_package['reviewed_live_ticker_validation_candidate_kind']}`",
        f"- Candidate status: `{review_package['reviewed_live_ticker_validation_candidate_status']}`",
        f"- Candidate digest: `{review_package['reviewed_live_ticker_validation_candidate_digest']}`",
        f"- Candidate checklist total/passed/failed/blockers: `{review_package['reviewed_live_ticker_validation_candidate_checklist_total']}`/`{review_package['reviewed_live_ticker_validation_candidate_checklist_passed']}`/`{review_package['reviewed_live_ticker_validation_candidate_checklist_failed']}`/`{review_package['reviewed_live_ticker_validation_candidate_blocker_count']}`",
        "",
        "## Source Evidence",
        f"- Ticker universe selection approval digest: `{review_package['ticker_universe_selection_approval_digest']}`",
        f"- Ticker universe selection candidate digest: `{review_package['ticker_universe_selection_candidate_digest']}`",
        f"- Ticker universe selection candidate review package digest: `{review_package['ticker_universe_selection_candidate_review_package_digest']}`",
        f"- Predictive evidence scope expansion plan candidate review package digest: `{review_package['predictive_evidence_scope_expansion_plan_candidate_review_package_digest']}`",
        f"- Predictive evidence scope expansion plan candidate digest: `{review_package['predictive_evidence_scope_expansion_plan_candidate_digest']}`",
        f"- Additional predictive evidence plan candidate review package digest: `{review_package['additional_predictive_evidence_plan_candidate_review_package_digest']}`",
        f"- Additional predictive evidence plan candidate digest: `{review_package['additional_predictive_evidence_plan_candidate_digest']}`",
        f"- Predictive usefulness acceptance readiness candidate review package digest: `{review_package['predictive_usefulness_acceptance_readiness_candidate_review_package_digest']}`",
        f"- Predictive usefulness acceptance readiness candidate digest: `{review_package['predictive_usefulness_acceptance_readiness_candidate_digest']}`",
        "",
        "## Validation Target Universe",
        f"- Approved expanded ticker count: `{review_package['approved_expanded_ticker_count']}`",
        f"- Validation target count: `{review_package['validation_target_count']}`",
        "- Validation targets: "
        + ", ".join(f"`{ticker}`" for ticker in review_package["approved_expanded_ticker_universe"]),
        f"- Target status: `{APPROVED_FOR_FUTURE_VALIDATION_ONLY}`",
        f"- Provider request status for every target: `{NOT_REQUESTED}`",
        f"- Live validation status for every target: `{NOT_PERFORMED}`",
        f"- Listing, security type, exchange, active, delisting, tradability, corporate-action, and historical aggregate availability statuses: `{NOT_VERIFIED}`",
        f"- Identity, split event, dividend event, acquisition, canonical dataset, and registry authority statuses: `{NOT_CREATED}`",
        f"- Research, runtime, strategy, paper trading, and broker execution use statuses: `{NOT_AUTHORIZED}`",
        "",
        "## Planned Validation Checks",
    ]
    lines.extend(f"- `{item['check_name']}`" for item in review_package["planned_validation_checks"])
    lines.extend(
        [
            "- Each planned check requires future provider interaction, was not performed now, and requires operator approval before execution.",
            "",
            "## Provider Request Policy",
        ]
    )
    for key, value in review_package["provider_request_policy"].items():
        lines.append(f"- {key}: `{value}`")
    lines.extend(["", "## Planned Outputs"])
    lines.extend(f"- `{item['output_id']}`" for item in review_package["planned_outputs"])
    lines.extend(
        [
            f"- All planned outputs remain `{PLANNED_NOT_GENERATED}` and `{RESEARCH_ONLY_NON_ACTIONABLE}`.",
            "",
            "## Future Gates",
        ]
    )
    lines.extend(f"- `{item}`" for item in review_package["future_gates"])
    lines.extend(["", "## Risk Controls"])
    lines.extend(f"- `{item}`" for item in review_package["risk_controls"])
    lines.extend(
        [
            "",
            "## Validation Boundary",
            f"- provider_requests_made_in_review: `{review_package['provider_requests_made_in_review']}`",
            f"- provider_request_authorized: `{review_package['provider_request_authorized']}`",
            f"- live_provider_transport_enabled: `{review_package['live_provider_transport_enabled']}`",
            f"- live_ticker_validation_authorized: `{review_package['live_ticker_validation_authorized']}`",
            f"- live_ticker_validation_performed: `{review_package['live_ticker_validation_performed']}`",
            f"- live_ticker_validation_approval_artifact_created: `{review_package['live_ticker_validation_approval_artifact_created']}`",
            f"- live_ticker_validation_artifact_created: `{review_package['live_ticker_validation_artifact_created']}`",
            f"- live_validation_results_created: `{review_package['live_validation_results_created']}`",
            "",
            "## Acquisition Boundary",
            f"- new_ticker_authority_created: `{review_package['new_ticker_authority_created']}`",
            f"- new_ticker_acquisition_authorized: `{review_package['new_ticker_acquisition_authorized']}`",
            f"- dataset_generation_authorized: `{review_package['dataset_generation_authorized']}`",
            f"- new_ticker_authority_artifact_created: `{review_package['new_ticker_authority_artifact_created']}`",
            f"- acquisition_authorization_artifact_created: `{review_package['acquisition_authorization_artifact_created']}`",
            f"- dataset_generation_authorization_created: `{review_package['dataset_generation_authorization_created']}`",
            "",
            "## Predictive/Profitability Boundary",
            f"- additional_predictive_evidence_execution_authorized: `{review_package['additional_predictive_evidence_execution_authorized']}`",
            f"- additional_predictive_evidence_executed: `{review_package['additional_predictive_evidence_executed']}`",
            f"- predictive_experiment_rerun_authorized: `{review_package['predictive_experiment_rerun_authorized']}`",
            f"- predictive_experiment_rerun_performed: `{review_package['predictive_experiment_rerun_performed']}`",
            f"- walk_forward_rerun_performed: `{review_package['walk_forward_rerun_performed']}`",
            f"- label_regeneration_performed: `{review_package['label_regeneration_performed']}`",
            f"- feature_matrix_regeneration_performed: `{review_package['feature_matrix_regeneration_performed']}`",
            f"- new_strategy_scoring_performed: `{review_package['new_strategy_scoring_performed']}`",
            f"- trade_recommendations_generated: `{review_package['trade_recommendations_generated']}`",
            f"- predictive_usefulness: `{review_package['predictive_usefulness']}`",
            f"- predictive_usefulness_acceptance_ready: `{review_package['predictive_usefulness_acceptance_ready']}`",
            f"- predictive_usefulness_acceptance_recommended: `{review_package['predictive_usefulness_acceptance_recommended']}`",
            f"- predictive_usefulness_acceptance_candidate_created: `{review_package['predictive_usefulness_acceptance_candidate_created']}`",
            f"- profitability: `{review_package['profitability']}`",
            f"- profitability_acceptance_ready: `{review_package['profitability_acceptance_ready']}`",
            f"- profitability_acceptance_recommended: `{review_package['profitability_acceptance_recommended']}`",
            "",
            "## Runtime Boundary",
            f"- runtime_migration_recommended: `{review_package['runtime_migration_recommended']}`",
            f"- runtime_migration_approved: `{review_package['runtime_migration_approved']}`",
            f"- runtime_migration_active: `{review_package['runtime_migration_active']}`",
            f"- strategy_runtime_migration: `{review_package['strategy_runtime_migration']}`",
            f"- runtime_use: `{review_package['runtime_use']}`",
            f"- strategy_use: `{review_package['strategy_use']}`",
            f"- paper_trading: `{review_package['paper_trading']}`",
            f"- broker_execution: `{review_package['broker_execution']}`",
            f"- automatic_stitching: `{review_package['automatic_stitching']}`",
            "",
            "## Checklist Summary",
            f"- Total checks: `{summary['total_checks']}`",
            f"- Passed checks: `{summary['passed_checks']}`",
            f"- Failed checks: `{summary['failed_checks']}`",
            f"- Blocker count: `{summary['blocker_count']}`",
            f"- ready_for_operator_assessment: `{summary['ready_for_operator_assessment']}`",
            f"- ready_for_live_ticker_validation_approval: `{summary['ready_for_live_ticker_validation_approval']}`",
            f"- live_ticker_validation_authorized: `{summary['live_ticker_validation_authorized']}`",
            f"- live_ticker_validation_performed: `{summary['live_ticker_validation_performed']}`",
            f"- new_ticker_authority_authorized: `{summary['new_ticker_authority_authorized']}`",
            f"- acquisition_authorized: `{summary['acquisition_authorized']}`",
            f"- dataset_generation_authorized: `{summary['dataset_generation_authorized']}`",
            f"- additional_predictive_evidence_execution_authorized: `{summary['additional_predictive_evidence_execution_authorized']}`",
            f"- predictive_usefulness_accepted: `{summary['predictive_usefulness_accepted']}`",
            f"- profitability_accepted: `{summary['profitability_accepted']}`",
            f"- runtime_migration_authorized: `{summary['runtime_migration_authorized']}`",
            f"- software_runtime_activation_authorized: `{summary['software_runtime_activation_authorized']}`",
            "",
            "## Guardrails",
            "- Default tests remain deterministic and offline.",
            "- No provider requests were made.",
            "- No provider data was fetched or validated.",
            "- No API keys, tokens, request headers, or environment values are recorded.",
            "- No live validation, authority, acquisition, predictive acceptance, profitability acceptance, runtime migration, paper trading, broker execution, or trade recommendation artifact is created.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_live_ticker_validation_candidate_review_package_v1(
    output_dir: str | Path,
    *,
    candidate: dict[str, Any] | None = None,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write the review package JSON to a new file without overwriting existing output."""
    review_package = build_live_ticker_validation_candidate_review_package_v1(candidate)
    validation = validate_live_ticker_validation_candidate_review_package_v1(review_package)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    output_name = filename or "live_ticker_validation_candidate_review_package_v1.json"
    target = output_path / output_name
    if target.exists():
        raise LiveTickerValidationCandidateReviewPackageError(
            f"output already exists: {_path_text(target)}"
        )
    payload_bytes = canonical_json_bytes(review_package)
    target.write_bytes(payload_bytes)
    return {
        "path": _path_text(target),
        "filename": output_name,
        "payload_sha256": sha256_bytes(payload_bytes),
        "payload_byte_size": len(payload_bytes),
        "live_ticker_validation_candidate_review_package_digest": validation[
            "live_ticker_validation_candidate_review_package_digest"
        ],
        "reviewed_live_ticker_validation_candidate_digest": validation[
            "reviewed_live_ticker_validation_candidate_digest"
        ],
        "status": review_package["review_status"],
        "provider_requests_made_in_review": False,
        "provider_request_authorized": False,
        "live_ticker_validation_authorized": False,
        "live_ticker_validation_performed": False,
    }
