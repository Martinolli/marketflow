"""Offline approval ceremony for predictive experiment execution."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    predictive_experiment_execution_candidate_operator_review_service as candidate_review,
)


ARTIFACT_KIND_PREDICTIVE_EXPERIMENT_EXECUTION_APPROVED = (
    "PREDICTIVE_EXPERIMENT_EXECUTION_APPROVED"
)
SCHEMA_VERSION_PREDICTIVE_EXPERIMENT_EXECUTION_APPROVAL_V1 = (
    "predictive_experiment_execution_approval_v1"
)
PREDICTIVE_EXPERIMENT_EXECUTION_APPROVED = "PREDICTIVE_EXPERIMENT_EXECUTION_APPROVED"
OPERATOR_DECISION_APPROVE_PREDICTIVE_EXPERIMENT_EXECUTION = (
    "APPROVE_PREDICTIVE_EXPERIMENT_EXECUTION"
)
OPERATOR_ATTESTATION_VERSION_V1 = (
    "predictive_experiment_execution_approval_operator_attestation_v1"
)
REQUIRED_PREDICTIVE_EXPERIMENT_EXECUTION_APPROVAL_ATTESTATION_PHRASE = (
    "APPROVE PREDICTIVE EXPERIMENT EXECUTION AAPL SWING POSITION_SWING "
    "2022-01-01 2025-12-31 RESEARCH_ONLY_NON_ACTIONABLE"
)

EXPECTED_EXECUTION_CANDIDATE_DIGEST = (
    candidate_review.EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_CANDIDATE_DIGEST
)
EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    "3541d8dc086c28dc3fac75e46e8982230889f958655ad14dc74dd647c8ed7e99"
)
EXPECTED_REVIEW_CHECKLIST_TOTAL = len(candidate_review.REQUIRED_CHECK_IDS)
EXPECTED_REVIEW_CHECKLIST_PASSED = len(candidate_review.REQUIRED_CHECK_IDS)
EXPECTED_REVIEW_CHECKLIST_FAILED = 0
EXPECTED_REVIEW_BLOCKER_COUNT = 0

PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

OPERATOR_CONFIRMATION_FIELDS = [
    "operator_confirms_research_only_scope",
    "operator_confirms_aapl_only",
    "operator_confirms_profiles_swing_and_position_swing",
    "operator_confirms_no_provider_requests_in_approval",
    "operator_confirms_no_experiment_execution_performed",
    "operator_confirms_no_walk_forward_validation_performed",
    "operator_confirms_no_label_generation_performed",
    "operator_confirms_no_feature_matrix_generation_performed",
    "operator_confirms_no_strategy_scoring_performed",
    "operator_confirms_no_trade_recommendations_generated",
    "operator_confirms_no_predictive_usefulness_acceptance",
    "operator_confirms_no_profitability_acceptance",
    "operator_confirms_no_runtime_migration_recommendation",
    "operator_confirms_no_runtime_migration_approval",
    "operator_confirms_no_runtime_activation",
    "operator_confirms_no_paper_trading",
    "operator_confirms_no_broker_execution",
]

REMAINING_ROADMAP_AFTER_EXECUTION_APPROVAL = [
    "Predictive experiment execution.",
    "Predictive experiment results review.",
    "Predictive usefulness review.",
    "Profitability review.",
    "Separate runtime migration approval ceremony, if ever authorized.",
]

REQUIRED_APPROVAL_CHECK_IDS = [
    "execution_candidate_review_digest_matches_expected",
    "execution_candidate_review_has_zero_blockers",
    "execution_candidate_digest_matches_expected",
    "execution_request_id_matches",
    "predictive_experiment_plan_digest_matches",
    "predictive_experiment_plan_review_digest_matches",
    "predictive_usefulness_candidate_digest_matches",
    "predictive_usefulness_candidate_review_digest_matches",
    "campaign_results_review_digest_matches",
    "campaign_execution_digest_matches",
    "swing_registry_approval_digest_matches",
    "position_swing_registry_approval_digest_matches",
    "experiment_scope_research_only",
    "ticker_universe_aapl_only",
    "profiles_swing_and_position_swing",
    "execution_mode_offline_research_experiment",
    "runtime_mode_not_runtime",
    "strategy_mode_not_strategy_input",
    "broker_mode_disabled",
    "paper_trading_mode_disabled",
    "planned_outputs_not_generated",
    "planned_outputs_research_only_non_actionable",
    "operator_decision_approved",
    "operator_attestation_phrase_matches",
    "operator_execution_candidate_digest_confirmation_matches",
    "operator_execution_candidate_review_digest_confirmation_matches",
    "operator_execution_request_id_confirmation_matches",
    "operator_predictive_experiment_plan_digest_confirmation_matches",
    "operator_predictive_experiment_plan_review_digest_confirmation_matches",
    "operator_predictive_usefulness_candidate_digest_confirmation_matches",
    "operator_predictive_usefulness_candidate_review_digest_confirmation_matches",
    "operator_campaign_results_review_digest_confirmation_matches",
    "operator_campaign_execution_digest_confirmation_matches",
    "operator_swing_registry_approval_digest_confirmation_matches",
    "operator_position_swing_registry_approval_digest_confirmation_matches",
    *OPERATOR_CONFIRMATION_FIELDS,
    "predictive_experiment_execution_authorized_true",
    "predictive_experiment_executed_false",
    "walk_forward_validation_performed_false",
    "out_of_sample_evaluation_performed_false",
    "label_generation_performed_false",
    "feature_matrix_generation_performed_false",
    "new_strategy_scoring_performed_false",
    "trade_recommendations_generated_false",
    "predictive_usefulness_not_accepted",
    "predictive_usefulness_acceptance_ready_false",
    "profitability_not_accepted",
    "profitability_acceptance_ready_false",
    "runtime_migration_recommended_false",
    "runtime_migration_approved_false",
    "runtime_migration_active_false",
    "strategy_runtime_migration_false",
    "runtime_use_not_authorized",
    "strategy_use_not_authorized",
    "paper_trading_not_authorized",
    "broker_execution_not_authorized",
    "automatic_stitching_false",
]


class PredictiveExperimentExecutionApprovalError(ValueError):
    """Raised when predictive experiment execution approval violates guardrails."""


def _check(check_id: str, expected: Any, actual: Any, *, severity: str = BLOCKER) -> dict[str, Any]:
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
        raise PredictiveExperimentExecutionApprovalError(f"{field_name} mismatch")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise PredictiveExperimentExecutionApprovalError(f"{field_name} must be true")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise PredictiveExperimentExecutionApprovalError(f"{field_name} must be false")


def build_predictive_experiment_execution_approval_attestation_v1(
    *,
    operator_reference: str,
    operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str,
    operator_confirms_execution_candidate_digest: str,
    operator_confirms_execution_candidate_review_package_digest: str,
    operator_confirms_execution_request_id: str,
    operator_confirms_predictive_experiment_plan_digest: str,
    operator_confirms_predictive_experiment_plan_review_package_digest: str,
    operator_confirms_predictive_usefulness_candidate_digest: str,
    operator_confirms_predictive_usefulness_candidate_review_package_digest: str,
    operator_confirms_campaign_results_review_digest: str,
    operator_confirms_campaign_execution_digest: str,
    operator_confirms_swing_registry_approval_digest: str,
    operator_confirms_position_swing_registry_approval_digest: str,
    operator_confirms_research_only_scope: bool,
    operator_confirms_aapl_only: bool,
    operator_confirms_profiles_swing_and_position_swing: bool,
    operator_confirms_no_provider_requests_in_approval: bool,
    operator_confirms_no_experiment_execution_performed: bool,
    operator_confirms_no_walk_forward_validation_performed: bool,
    operator_confirms_no_label_generation_performed: bool,
    operator_confirms_no_feature_matrix_generation_performed: bool,
    operator_confirms_no_strategy_scoring_performed: bool,
    operator_confirms_no_trade_recommendations_generated: bool,
    operator_confirms_no_predictive_usefulness_acceptance: bool,
    operator_confirms_no_profitability_acceptance: bool,
    operator_confirms_no_runtime_migration_recommendation: bool,
    operator_confirms_no_runtime_migration_approval: bool,
    operator_confirms_no_runtime_activation: bool,
    operator_confirms_no_paper_trading: bool,
    operator_confirms_no_broker_execution: bool,
    operator_decision: str = OPERATOR_DECISION_APPROVE_PREDICTIVE_EXPERIMENT_EXECUTION,
    operator_attestation_version: str = OPERATOR_ATTESTATION_VERSION_V1,
) -> dict[str, Any]:
    """Build a non-secret operator attestation for predictive experiment approval."""
    return {
        "operator_reference": operator_reference,
        "operator_decision": operator_decision,
        "operator_attestation_phrase": operator_attestation_phrase,
        "operator_attestation_timestamp_utc": operator_attestation_timestamp_utc,
        "operator_attestation_version": operator_attestation_version,
        "operator_confirms_execution_candidate_digest": operator_confirms_execution_candidate_digest,
        "operator_confirms_execution_candidate_review_package_digest": (
            operator_confirms_execution_candidate_review_package_digest
        ),
        "operator_confirms_execution_request_id": operator_confirms_execution_request_id,
        "operator_confirms_predictive_experiment_plan_digest": (
            operator_confirms_predictive_experiment_plan_digest
        ),
        "operator_confirms_predictive_experiment_plan_review_package_digest": (
            operator_confirms_predictive_experiment_plan_review_package_digest
        ),
        "operator_confirms_predictive_usefulness_candidate_digest": (
            operator_confirms_predictive_usefulness_candidate_digest
        ),
        "operator_confirms_predictive_usefulness_candidate_review_package_digest": (
            operator_confirms_predictive_usefulness_candidate_review_package_digest
        ),
        "operator_confirms_campaign_results_review_digest": (
            operator_confirms_campaign_results_review_digest
        ),
        "operator_confirms_campaign_execution_digest": operator_confirms_campaign_execution_digest,
        "operator_confirms_swing_registry_approval_digest": (
            operator_confirms_swing_registry_approval_digest
        ),
        "operator_confirms_position_swing_registry_approval_digest": (
            operator_confirms_position_swing_registry_approval_digest
        ),
        **{field: locals()[field] for field in OPERATOR_CONFIRMATION_FIELDS},
    }


def _source_review_package(review_package: dict[str, Any] | None) -> dict[str, Any]:
    source_review = (
        deepcopy(review_package)
        if review_package is not None
        else candidate_review.build_predictive_experiment_execution_candidate_review_package_v1()
    )
    try:
        validation = (
            candidate_review.validate_predictive_experiment_execution_candidate_review_package_v1(
                source_review
            )
        )
    except candidate_review.PredictiveExperimentExecutionCandidateReviewPackageError as exc:
        raise PredictiveExperimentExecutionApprovalError(
            f"source execution candidate review package invalid: {exc}"
        ) from exc
    _expect(
        validation["predictive_experiment_execution_candidate_review_package_digest"],
        EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "source execution candidate review package digest",
    )
    _expect(
        source_review["review_summary"]["failed_checks"],
        0,
        "source execution candidate review failed check count",
    )
    _expect(
        source_review["review_summary"]["blocker_count"],
        0,
        "source execution candidate review blocker count",
    )
    return source_review


def _review_evidence(source_review: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_execution_candidate_kind": source_review["reviewed_execution_candidate_kind"],
        "source_execution_candidate_status": source_review["reviewed_execution_candidate_status"],
        "source_execution_candidate_digest": source_review[
            "reviewed_execution_candidate_digest"
        ],
        "source_execution_candidate_review_package_kind": source_review["artifact_kind"],
        "source_execution_candidate_review_status": source_review["review_status"],
        "source_execution_candidate_review_package_digest": source_review[
            "predictive_experiment_execution_candidate_review_package_digest"
        ],
        "source_execution_candidate_review_checklist_total": source_review["review_summary"][
            "total_checks"
        ],
        "source_execution_candidate_review_checklist_passed": source_review["review_summary"][
            "passed_checks"
        ],
        "source_execution_candidate_review_checklist_failed": source_review["review_summary"][
            "failed_checks"
        ],
        "source_execution_candidate_review_blocker_count": source_review["review_summary"][
            "blocker_count"
        ],
        "predictive_experiment_execution_request_id": source_review[
            "predictive_experiment_execution_request_id"
        ],
        "experiment_scope": source_review["experiment_scope"],
        "ticker_universe": list(source_review["ticker_universe"]),
        "dataset_profiles": list(source_review["dataset_profiles"]),
        "date_range_start": source_review["date_range_start"],
        "date_range_end": source_review["date_range_end"],
        "execution_mode": source_review["execution_mode"],
        "runtime_mode": source_review["runtime_mode"],
        "strategy_mode": source_review["strategy_mode"],
        "broker_mode": source_review["broker_mode"],
        "paper_trading_mode": source_review["paper_trading_mode"],
        "planned_output_count": source_review["planned_output_count"],
        "planned_outputs_status": source_review["planned_outputs_status"],
        "planned_outputs_label": source_review["planned_outputs_label"],
        "planned_outputs": deepcopy(source_review["planned_outputs"]),
        "predictive_experiment_plan_digest": source_review["predictive_experiment_plan_digest"],
        "predictive_experiment_plan_review_package_digest": source_review[
            "predictive_experiment_plan_review_package_digest"
        ],
        "predictive_usefulness_review_candidate_digest": source_review[
            "predictive_usefulness_review_candidate_digest"
        ],
        "predictive_usefulness_review_candidate_review_package_digest": source_review[
            "predictive_usefulness_review_candidate_review_package_digest"
        ],
        "campaign_results_review_package_digest": source_review[
            "campaign_execution_results_review_package_digest"
        ],
        "campaign_execution_digest": source_review["campaign_execution_digest"],
        "swing_registry_approval_digest": source_review["swing_registry_approval_digest"],
        "position_swing_registry_approval_digest": source_review[
            "position_swing_registry_approval_digest"
        ],
    }


def _attestation_checks(attestation: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not isinstance(attestation, dict):
        return [
            _check("operator_decision_approved", OPERATOR_DECISION_APPROVE_PREDICTIVE_EXPERIMENT_EXECUTION, None),
            _check("operator_attestation_phrase_matches", REQUIRED_PREDICTIVE_EXPERIMENT_EXECUTION_APPROVAL_ATTESTATION_PHRASE, None),
            _check("operator_execution_candidate_digest_confirmation_matches", EXPECTED_EXECUTION_CANDIDATE_DIGEST, None),
            _check("operator_execution_candidate_review_digest_confirmation_matches", EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST, None),
            _check("operator_execution_request_id_confirmation_matches", candidate_review.candidate_service.PREDICTIVE_EXPERIMENT_EXECUTION_REQUEST_ID, None),
            _check("operator_predictive_experiment_plan_digest_confirmation_matches", candidate_review.candidate_service.EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_DIGEST, None),
            _check("operator_predictive_experiment_plan_review_digest_confirmation_matches", candidate_review.candidate_service.EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_REVIEW_PACKAGE_DIGEST, None),
            _check("operator_predictive_usefulness_candidate_digest_confirmation_matches", candidate_review.candidate_service.plan_review_service.plan_service.EXPECTED_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_DIGEST, None),
            _check("operator_predictive_usefulness_candidate_review_digest_confirmation_matches", candidate_review.candidate_service.plan_review_service.plan_service.EXPECTED_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_REVIEW_PACKAGE_DIGEST, None),
            _check("operator_campaign_results_review_digest_confirmation_matches", candidate_review.candidate_service.plan_review_service.plan_service.EXPECTED_CAMPAIGN_EXECUTION_RESULTS_REVIEW_PACKAGE_DIGEST, None),
            _check("operator_campaign_execution_digest_confirmation_matches", candidate_review.candidate_service.plan_review_service.plan_service.EXPECTED_CAMPAIGN_EXECUTION_DIGEST, None),
            _check("operator_swing_registry_approval_digest_confirmation_matches", candidate_review.candidate_service.plan_review_service.plan_service.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST, None),
            _check("operator_position_swing_registry_approval_digest_confirmation_matches", candidate_review.candidate_service.plan_review_service.plan_service.EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST, None),
            *[_check(field, True, None) for field in OPERATOR_CONFIRMATION_FIELDS],
        ]
    return [
        _check("operator_decision_approved", OPERATOR_DECISION_APPROVE_PREDICTIVE_EXPERIMENT_EXECUTION, attestation.get("operator_decision")),
        _check("operator_attestation_phrase_matches", REQUIRED_PREDICTIVE_EXPERIMENT_EXECUTION_APPROVAL_ATTESTATION_PHRASE, attestation.get("operator_attestation_phrase")),
        _check("operator_execution_candidate_digest_confirmation_matches", EXPECTED_EXECUTION_CANDIDATE_DIGEST, attestation.get("operator_confirms_execution_candidate_digest")),
        _check("operator_execution_candidate_review_digest_confirmation_matches", EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST, attestation.get("operator_confirms_execution_candidate_review_package_digest")),
        _check("operator_execution_request_id_confirmation_matches", candidate_review.candidate_service.PREDICTIVE_EXPERIMENT_EXECUTION_REQUEST_ID, attestation.get("operator_confirms_execution_request_id")),
        _check("operator_predictive_experiment_plan_digest_confirmation_matches", candidate_review.candidate_service.EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_DIGEST, attestation.get("operator_confirms_predictive_experiment_plan_digest")),
        _check("operator_predictive_experiment_plan_review_digest_confirmation_matches", candidate_review.candidate_service.EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_REVIEW_PACKAGE_DIGEST, attestation.get("operator_confirms_predictive_experiment_plan_review_package_digest")),
        _check("operator_predictive_usefulness_candidate_digest_confirmation_matches", candidate_review.candidate_service.plan_review_service.plan_service.EXPECTED_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_DIGEST, attestation.get("operator_confirms_predictive_usefulness_candidate_digest")),
        _check("operator_predictive_usefulness_candidate_review_digest_confirmation_matches", candidate_review.candidate_service.plan_review_service.plan_service.EXPECTED_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_REVIEW_PACKAGE_DIGEST, attestation.get("operator_confirms_predictive_usefulness_candidate_review_package_digest")),
        _check("operator_campaign_results_review_digest_confirmation_matches", candidate_review.candidate_service.plan_review_service.plan_service.EXPECTED_CAMPAIGN_EXECUTION_RESULTS_REVIEW_PACKAGE_DIGEST, attestation.get("operator_confirms_campaign_results_review_digest")),
        _check("operator_campaign_execution_digest_confirmation_matches", candidate_review.candidate_service.plan_review_service.plan_service.EXPECTED_CAMPAIGN_EXECUTION_DIGEST, attestation.get("operator_confirms_campaign_execution_digest")),
        _check("operator_swing_registry_approval_digest_confirmation_matches", candidate_review.candidate_service.plan_review_service.plan_service.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST, attestation.get("operator_confirms_swing_registry_approval_digest")),
        _check("operator_position_swing_registry_approval_digest_confirmation_matches", candidate_review.candidate_service.plan_review_service.plan_service.EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST, attestation.get("operator_confirms_position_swing_registry_approval_digest")),
        *[_check(field, True, attestation.get(field)) for field in OPERATOR_CONFIRMATION_FIELDS],
    ]


def _validated_operator_attestation(attestation: dict[str, Any] | None) -> dict[str, Any]:
    checks = _attestation_checks(attestation)
    failed = [item for item in checks if item["status"] != PASS]
    if failed:
        raise PredictiveExperimentExecutionApprovalError(
            f"operator attestation failed check: {failed[0]['check_id']}"
        )
    if not isinstance(attestation, dict):
        raise PredictiveExperimentExecutionApprovalError("operator_attestation missing")
    for field in (
        "operator_reference",
        "operator_attestation_timestamp_utc",
        "operator_attestation_version",
    ):
        if not isinstance(attestation.get(field), str) or not attestation[field]:
            raise PredictiveExperimentExecutionApprovalError(f"{field} missing")
    return attestation


def _approval_checklist(approved: dict[str, Any]) -> list[dict[str, Any]]:
    attestation = approved.get("operator_attestation")
    return [
        _check("execution_candidate_review_digest_matches_expected", EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST, approved.get("source_execution_candidate_review_package_digest")),
        _check("execution_candidate_review_has_zero_blockers", 0, approved.get("source_execution_candidate_review_blocker_count")),
        _check("execution_candidate_digest_matches_expected", EXPECTED_EXECUTION_CANDIDATE_DIGEST, approved.get("source_execution_candidate_digest")),
        _check("execution_request_id_matches", candidate_review.candidate_service.PREDICTIVE_EXPERIMENT_EXECUTION_REQUEST_ID, approved.get("predictive_experiment_execution_request_id")),
        _check("predictive_experiment_plan_digest_matches", candidate_review.candidate_service.EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_DIGEST, approved.get("predictive_experiment_plan_digest")),
        _check("predictive_experiment_plan_review_digest_matches", candidate_review.candidate_service.EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_REVIEW_PACKAGE_DIGEST, approved.get("predictive_experiment_plan_review_package_digest")),
        _check("predictive_usefulness_candidate_digest_matches", candidate_review.candidate_service.plan_review_service.plan_service.EXPECTED_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_DIGEST, approved.get("predictive_usefulness_review_candidate_digest")),
        _check("predictive_usefulness_candidate_review_digest_matches", candidate_review.candidate_service.plan_review_service.plan_service.EXPECTED_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_REVIEW_PACKAGE_DIGEST, approved.get("predictive_usefulness_review_candidate_review_package_digest")),
        _check("campaign_results_review_digest_matches", candidate_review.candidate_service.plan_review_service.plan_service.EXPECTED_CAMPAIGN_EXECUTION_RESULTS_REVIEW_PACKAGE_DIGEST, approved.get("campaign_results_review_package_digest")),
        _check("campaign_execution_digest_matches", candidate_review.candidate_service.plan_review_service.plan_service.EXPECTED_CAMPAIGN_EXECUTION_DIGEST, approved.get("campaign_execution_digest")),
        _check("swing_registry_approval_digest_matches", candidate_review.candidate_service.plan_review_service.plan_service.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST, approved.get("swing_registry_approval_digest")),
        _check("position_swing_registry_approval_digest_matches", candidate_review.candidate_service.plan_review_service.plan_service.EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST, approved.get("position_swing_registry_approval_digest")),
        _check("experiment_scope_research_only", "RESEARCH_ONLY", approved.get("experiment_scope")),
        _check("ticker_universe_aapl_only", ["AAPL"], approved.get("ticker_universe")),
        _check("profiles_swing_and_position_swing", ["SWING", "POSITION_SWING"], [item.get("profile") for item in approved.get("dataset_profiles", []) if isinstance(item, dict)]),
        _check("execution_mode_offline_research_experiment", "OFFLINE_RESEARCH_EXPERIMENT", approved.get("execution_mode")),
        _check("runtime_mode_not_runtime", "NOT_RUNTIME", approved.get("runtime_mode")),
        _check("strategy_mode_not_strategy_input", "NOT_STRATEGY_INPUT", approved.get("strategy_mode")),
        _check("broker_mode_disabled", "DISABLED", approved.get("broker_mode")),
        _check("paper_trading_mode_disabled", "DISABLED", approved.get("paper_trading_mode")),
        _check("planned_outputs_not_generated", candidate_review.candidate_service.PLANNED_NOT_GENERATED, approved.get("planned_outputs_status")),
        _check("planned_outputs_research_only_non_actionable", candidate_review.candidate_service.RESEARCH_ONLY_NON_ACTIONABLE, approved.get("planned_outputs_label")),
        *_attestation_checks(attestation),
        _check("predictive_experiment_execution_authorized_true", True, approved.get("predictive_experiment_execution_authorized")),
        _check("predictive_experiment_executed_false", False, approved.get("predictive_experiment_executed")),
        _check("walk_forward_validation_performed_false", False, approved.get("walk_forward_validation_performed")),
        _check("out_of_sample_evaluation_performed_false", False, approved.get("out_of_sample_evaluation_performed")),
        _check("label_generation_performed_false", False, approved.get("label_generation_performed")),
        _check("feature_matrix_generation_performed_false", False, approved.get("feature_matrix_generation_performed")),
        _check("new_strategy_scoring_performed_false", False, approved.get("new_strategy_scoring_performed")),
        _check("trade_recommendations_generated_false", False, approved.get("trade_recommendations_generated")),
        _check("predictive_usefulness_not_accepted", candidate_review.candidate_service.plan_review_service.plan_service.acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED, approved.get("predictive_usefulness")),
        _check("predictive_usefulness_acceptance_ready_false", False, approved.get("predictive_usefulness_acceptance_ready")),
        _check("profitability_not_accepted", candidate_review.candidate_service.plan_review_service.plan_service.acquisition.PROFITABILITY_NOT_ACCEPTED, approved.get("profitability")),
        _check("profitability_acceptance_ready_false", False, approved.get("profitability_acceptance_ready")),
        _check("runtime_migration_recommended_false", False, approved.get("runtime_migration_recommended")),
        _check("runtime_migration_approved_false", False, approved.get("runtime_migration_approved")),
        _check("runtime_migration_active_false", False, approved.get("runtime_migration_active")),
        _check("strategy_runtime_migration_false", False, approved.get("strategy_runtime_migration")),
        _check("runtime_use_not_authorized", candidate_review.candidate_service.NOT_AUTHORIZED, approved.get("runtime_use")),
        _check("strategy_use_not_authorized", candidate_review.candidate_service.NOT_AUTHORIZED, approved.get("strategy_use")),
        _check("paper_trading_not_authorized", candidate_review.candidate_service.NOT_AUTHORIZED, approved.get("paper_trading")),
        _check("broker_execution_not_authorized", candidate_review.candidate_service.NOT_AUTHORIZED, approved.get("broker_execution")),
        _check("automatic_stitching_false", False, approved.get("automatic_stitching")),
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
        "predictive_experiment_execution_authorized_by_operator": failed == 0,
        "predictive_experiment_executed": False,
        "software_predictive_usefulness_authorized": False,
        "software_profitability_authorized": False,
        "software_runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def _digest_payload(approved: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(approved)
    payload.pop("predictive_experiment_execution_approval_digest", None)
    return payload


def predictive_experiment_execution_approval_digest_v1(approved: dict[str, Any]) -> str:
    """Return the deterministic semantic digest for the predictive execution approval."""
    return semantic_digest(_digest_payload(approved))


def build_predictive_experiment_execution_approved_v1(
    *,
    execution_candidate_review_package: dict[str, Any] | None = None,
    operator_attestation: dict[str, Any],
) -> dict[str, Any]:
    """Build the approved artifact without executing a predictive experiment."""
    attestation = _validated_operator_attestation(operator_attestation)
    source_review = _source_review_package(execution_candidate_review_package)
    approved = {
        "artifact_kind": ARTIFACT_KIND_PREDICTIVE_EXPERIMENT_EXECUTION_APPROVED,
        "schema_version": SCHEMA_VERSION_PREDICTIVE_EXPERIMENT_EXECUTION_APPROVAL_V1,
        "approval_status": PREDICTIVE_EXPERIMENT_EXECUTION_APPROVED,
        "predictive_experiment_execution_authorized": True,
        "predictive_experiment_executed": False,
        "walk_forward_validation_performed": False,
        "out_of_sample_evaluation_performed": False,
        "label_generation_performed": False,
        "feature_matrix_generation_performed": False,
        "new_strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "research_only": True,
        "created_offline": True,
        "provider_requests_made_in_approval": False,
        "predictive_usefulness": (
            candidate_review.candidate_service.plan_review_service.plan_service.acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED
        ),
        "predictive_usefulness_acceptance_ready": False,
        "profitability": (
            candidate_review.candidate_service.plan_review_service.plan_service.acquisition.PROFITABILITY_NOT_ACCEPTED
        ),
        "profitability_acceptance_ready": False,
        "runtime_migration_recommended": False,
        "runtime_migration_approved": False,
        "runtime_migration_active": False,
        "strategy_runtime_migration": False,
        "runtime_use": candidate_review.candidate_service.NOT_AUTHORIZED,
        "strategy_use": candidate_review.candidate_service.NOT_AUTHORIZED,
        "paper_trading": candidate_review.candidate_service.NOT_AUTHORIZED,
        "broker_execution": candidate_review.candidate_service.NOT_AUTHORIZED,
        "automatic_stitching": False,
        "operator_attestation": attestation,
        "remaining_roadmap": list(REMAINING_ROADMAP_AFTER_EXECUTION_APPROVAL),
        **_review_evidence(source_review),
    }
    checklist = _approval_checklist(approved)
    approved["approval_checklist"] = checklist
    approved["approval_summary"] = _summary(checklist)
    approved["predictive_experiment_execution_approval_digest"] = (
        predictive_experiment_execution_approval_digest_v1(approved)
    )
    validate_predictive_experiment_execution_approved_v1(approved)
    return approved


def _reject_forbidden_values(mapping: dict[str, Any], *, path: str = "approved_artifact") -> None:
    for key, value in mapping.items():
        current_path = f"{path}.{key}"
        if isinstance(value, str) and value in {
            "PREDICTIVE_EXPERIMENT_EXECUTED",
            "WALK_FORWARD_VALIDATION_EXECUTED",
            "PREDICTIVE_USEFULNESS_ACCEPTED",
            "PROFITABILITY_ACCEPTED",
            "RUNTIME_MIGRATION_APPROVED",
            "RUNTIME_MIGRATION_ACTIVE",
            "STRATEGY_RUNTIME_MIGRATION",
        }:
            raise PredictiveExperimentExecutionApprovalError(
                f"{current_path} must not emit {value}"
            )
        if key in {
            "predictive_experiment_executed",
            "walk_forward_validation_performed",
            "out_of_sample_evaluation_performed",
            "label_generation_performed",
            "feature_matrix_generation_performed",
            "new_strategy_scoring_performed",
            "trade_recommendations_generated",
            "predictive_usefulness_acceptance_ready",
            "profitability_acceptance_ready",
            "runtime_migration_recommended",
            "runtime_migration_approved",
            "runtime_migration_active",
            "strategy_runtime_migration",
            "automatic_stitching",
            "provider_requests_made_in_approval",
            "generated",
            "execution_performed",
            "output_generated",
        } and value is True:
            raise PredictiveExperimentExecutionApprovalError(f"{current_path} must be false")
        if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and value == "AUTHORIZED":
            raise PredictiveExperimentExecutionApprovalError(
                f"{current_path} must not be AUTHORIZED"
            )
        if key in {"predictive_usefulness", "profitability"} and value == "accepted":
            raise PredictiveExperimentExecutionApprovalError(
                f"{current_path} must not be accepted"
            )
        if isinstance(value, dict):
            _reject_forbidden_values(value, path=current_path)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, dict):
                    _reject_forbidden_values(item, path=f"{current_path}[{index}]")


def validate_predictive_experiment_execution_approved_v1(
    approved_artifact: dict[str, Any],
) -> dict[str, Any]:
    """Validate approval while preserving all execution-result and runtime guardrails."""
    if not isinstance(approved_artifact, dict):
        raise PredictiveExperimentExecutionApprovalError(
            "approved artifact must be a JSON object"
        )
    _reject_forbidden_values(approved_artifact)
    _expect(
        approved_artifact.get("artifact_kind"),
        ARTIFACT_KIND_PREDICTIVE_EXPERIMENT_EXECUTION_APPROVED,
        "artifact_kind",
    )
    _expect(
        approved_artifact.get("schema_version"),
        SCHEMA_VERSION_PREDICTIVE_EXPERIMENT_EXECUTION_APPROVAL_V1,
        "schema_version",
    )
    _expect(
        approved_artifact.get("approval_status"),
        PREDICTIVE_EXPERIMENT_EXECUTION_APPROVED,
        "approval_status",
    )
    for field in (
        "predictive_experiment_execution_authorized",
        "research_only",
        "created_offline",
    ):
        _expect_true(approved_artifact.get(field), field)
    for field in (
        "predictive_experiment_executed",
        "walk_forward_validation_performed",
        "out_of_sample_evaluation_performed",
        "label_generation_performed",
        "feature_matrix_generation_performed",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
        "provider_requests_made_in_approval",
        "predictive_usefulness_acceptance_ready",
        "profitability_acceptance_ready",
        "runtime_migration_recommended",
        "runtime_migration_approved",
        "runtime_migration_active",
        "strategy_runtime_migration",
        "automatic_stitching",
    ):
        _expect_false(approved_artifact.get(field), field)
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(approved_artifact.get(field), candidate_review.candidate_service.NOT_AUTHORIZED, field)
    for field, expected in {
        "predictive_usefulness": candidate_review.candidate_service.plan_review_service.plan_service.acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": candidate_review.candidate_service.plan_review_service.plan_service.acquisition.PROFITABILITY_NOT_ACCEPTED,
        "source_execution_candidate_kind": candidate_review.candidate_service.ARTIFACT_KIND_PREDICTIVE_EXPERIMENT_EXECUTION_CANDIDATE,
        "source_execution_candidate_status": candidate_review.candidate_service.PREDICTIVE_EXPERIMENT_EXECUTION_READY_FOR_OPERATOR_REVIEW,
        "source_execution_candidate_digest": EXPECTED_EXECUTION_CANDIDATE_DIGEST,
        "source_execution_candidate_review_package_kind": candidate_review.ARTIFACT_KIND_PREDICTIVE_EXPERIMENT_EXECUTION_CANDIDATE_REVIEW_PACKAGE,
        "source_execution_candidate_review_status": candidate_review.PREDICTIVE_EXPERIMENT_EXECUTION_CANDIDATE_REVIEW_PACKAGE_READY,
        "source_execution_candidate_review_package_digest": EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "source_execution_candidate_review_checklist_total": EXPECTED_REVIEW_CHECKLIST_TOTAL,
        "source_execution_candidate_review_checklist_passed": EXPECTED_REVIEW_CHECKLIST_PASSED,
        "source_execution_candidate_review_checklist_failed": EXPECTED_REVIEW_CHECKLIST_FAILED,
        "source_execution_candidate_review_blocker_count": EXPECTED_REVIEW_BLOCKER_COUNT,
        "predictive_experiment_execution_request_id": candidate_review.candidate_service.PREDICTIVE_EXPERIMENT_EXECUTION_REQUEST_ID,
        "experiment_scope": "RESEARCH_ONLY",
        "ticker_universe": ["AAPL"],
        "date_range_start": "2022-01-01",
        "date_range_end": "2025-12-31",
        "execution_mode": "OFFLINE_RESEARCH_EXPERIMENT",
        "runtime_mode": "NOT_RUNTIME",
        "strategy_mode": "NOT_STRATEGY_INPUT",
        "broker_mode": "DISABLED",
        "paper_trading_mode": "DISABLED",
        "planned_output_count": 13,
        "planned_outputs_status": candidate_review.candidate_service.PLANNED_NOT_GENERATED,
        "planned_outputs_label": candidate_review.candidate_service.RESEARCH_ONLY_NON_ACTIONABLE,
        "predictive_experiment_plan_digest": candidate_review.candidate_service.EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_DIGEST,
        "predictive_experiment_plan_review_package_digest": candidate_review.candidate_service.EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_REVIEW_PACKAGE_DIGEST,
        "predictive_usefulness_review_candidate_digest": candidate_review.candidate_service.plan_review_service.plan_service.EXPECTED_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_DIGEST,
        "predictive_usefulness_review_candidate_review_package_digest": candidate_review.candidate_service.plan_review_service.plan_service.EXPECTED_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "campaign_results_review_package_digest": candidate_review.candidate_service.plan_review_service.plan_service.EXPECTED_CAMPAIGN_EXECUTION_RESULTS_REVIEW_PACKAGE_DIGEST,
        "campaign_execution_digest": candidate_review.candidate_service.plan_review_service.plan_service.EXPECTED_CAMPAIGN_EXECUTION_DIGEST,
        "swing_registry_approval_digest": candidate_review.candidate_service.plan_review_service.plan_service.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST,
        "position_swing_registry_approval_digest": candidate_review.candidate_service.plan_review_service.plan_service.EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST,
        "remaining_roadmap": REMAINING_ROADMAP_AFTER_EXECUTION_APPROVAL,
    }.items():
        _expect(approved_artifact.get(field), expected, field)
    _expect(
        [item.get("profile") for item in approved_artifact.get("dataset_profiles", []) if isinstance(item, dict)],
        ["SWING", "POSITION_SWING"],
        "dataset_profiles",
    )
    _validated_operator_attestation(approved_artifact.get("operator_attestation"))
    checklist = _approval_checklist(approved_artifact)
    _expect([item["check_id"] for item in checklist], REQUIRED_APPROVAL_CHECK_IDS, "approval_checklist check IDs")
    failed = [item for item in checklist if item["status"] != PASS]
    if failed:
        raise PredictiveExperimentExecutionApprovalError(
            f"approval checklist contains failed check: {failed[0]['check_id']}"
        )
    _expect(approved_artifact.get("approval_checklist"), checklist, "approval_checklist")
    summary = _summary(checklist)
    _expect(approved_artifact.get("approval_summary"), summary, "approval_summary")
    _expect_true(
        summary.get("predictive_experiment_execution_authorized_by_operator"),
        "predictive_experiment_execution_authorized_by_operator",
    )
    _expect_false(
        summary.get("predictive_experiment_executed"),
        "predictive_experiment_executed",
    )
    _expect_false(
        summary.get("software_runtime_migration_authorized"),
        "software_runtime_migration_authorized",
    )
    _expect_false(
        summary.get("software_runtime_activation_authorized"),
        "software_runtime_activation_authorized",
    )
    _expect_false(
        summary.get("software_predictive_usefulness_authorized"),
        "software_predictive_usefulness_authorized",
    )
    _expect_false(summary.get("software_profitability_authorized"), "software_profitability_authorized")
    digest = approved_artifact.get("predictive_experiment_execution_approval_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise PredictiveExperimentExecutionApprovalError(
            "predictive_experiment_execution_approval_digest missing"
        )
    _expect(
        digest,
        predictive_experiment_execution_approval_digest_v1(approved_artifact),
        "predictive_experiment_execution_approval_digest",
    )
    return {
        "status": "PREDICTIVE_EXPERIMENT_EXECUTION_APPROVED_VALID",
        "artifact_kind": approved_artifact["artifact_kind"],
        "approval_status": approved_artifact["approval_status"],
        "predictive_experiment_execution_approval_digest": digest,
        "predictive_experiment_execution_request_id": (
            candidate_review.candidate_service.PREDICTIVE_EXPERIMENT_EXECUTION_REQUEST_ID
        ),
        "source_execution_candidate_digest": EXPECTED_EXECUTION_CANDIDATE_DIGEST,
        "source_execution_candidate_review_package_digest": (
            EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "predictive_experiment_plan_digest": approved_artifact[
            "predictive_experiment_plan_digest"
        ],
        "predictive_experiment_plan_review_package_digest": approved_artifact[
            "predictive_experiment_plan_review_package_digest"
        ],
        "campaign_results_review_package_digest": approved_artifact[
            "campaign_results_review_package_digest"
        ],
        "predictive_experiment_execution_authorized": True,
        "predictive_experiment_executed": False,
        "walk_forward_validation_performed": False,
        "label_generation_performed": False,
        "feature_matrix_generation_performed": False,
        "new_strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "runtime_migration_recommended": False,
        "runtime_migration_approved": False,
        "runtime_migration_active": False,
        "runtime_use": candidate_review.candidate_service.NOT_AUTHORIZED,
        "strategy_use": candidate_review.candidate_service.NOT_AUTHORIZED,
        "paper_trading": candidate_review.candidate_service.NOT_AUTHORIZED,
        "broker_execution": candidate_review.candidate_service.NOT_AUTHORIZED,
        "predictive_usefulness": (
            candidate_review.candidate_service.plan_review_service.plan_service.acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED
        ),
        "profitability": (
            candidate_review.candidate_service.plan_review_service.plan_service.acquisition.PROFITABILITY_NOT_ACCEPTED
        ),
        "total_checks": summary["total_checks"],
        "passed_checks": summary["passed_checks"],
        "failed_checks": summary["failed_checks"],
        "blocker_count": summary["blocker_count"],
    }


def build_predictive_experiment_execution_approved_markdown_v1(
    approved_artifact: dict[str, Any],
) -> str:
    """Render a sanitized predictive experiment execution approval status document."""
    validation = validate_predictive_experiment_execution_approved_v1(approved_artifact)
    attestation = approved_artifact["operator_attestation"]
    summary = approved_artifact["approval_summary"]
    lines = [
        "# MarketFlow Predictive Experiment Execution Approval Status",
        "",
        "## Title",
        "- Predictive Experiment Execution Approval Ceremony v1.",
        "",
        "## Approved Predictive Experiment Execution",
        f"- Artifact kind: `{approved_artifact['artifact_kind']}`",
        f"- Approval status: `{approved_artifact['approval_status']}`",
        f"- Execution request ID: `{approved_artifact['predictive_experiment_execution_request_id']}`",
        f"- Execution authorized: `{approved_artifact['predictive_experiment_execution_authorized']}`",
        f"- Execution performed: `{approved_artifact['predictive_experiment_executed']}`",
        f"- Approval digest: `{validation['predictive_experiment_execution_approval_digest']}`",
        "",
        "## Operator Attestation",
        f"- Operator reference: `{attestation['operator_reference']}`",
        f"- Operator decision: `{attestation['operator_decision']}`",
        f"- Attestation timestamp UTC: `{attestation['operator_attestation_timestamp_utc']}`",
        f"- Attestation version: `{attestation['operator_attestation_version']}`",
        "",
        "## Source Execution Candidate Review Package",
        f"- Review package kind: `{approved_artifact['source_execution_candidate_review_package_kind']}`",
        f"- Review status: `{approved_artifact['source_execution_candidate_review_status']}`",
        f"- Review package digest: `{approved_artifact['source_execution_candidate_review_package_digest']}`",
        f"- Execution candidate digest: `{approved_artifact['source_execution_candidate_digest']}`",
        f"- Review blockers: `{approved_artifact['source_execution_candidate_review_blocker_count']}`",
        "",
        "## Experiment Scope",
        f"- Scope: `{approved_artifact['experiment_scope']}`",
        f"- Ticker universe: `{', '.join(approved_artifact['ticker_universe'])}`",
        f"- Date range: `{approved_artifact['date_range_start']}` through `{approved_artifact['date_range_end']}`",
        f"- Execution mode: `{approved_artifact['execution_mode']}`",
        "",
        "## Execution Boundary",
        f"- predictive_experiment_execution_authorized: `{approved_artifact['predictive_experiment_execution_authorized']}`",
        f"- predictive_experiment_executed: `{approved_artifact['predictive_experiment_executed']}`",
        f"- walk_forward_validation_performed: `{approved_artifact['walk_forward_validation_performed']}`",
        f"- label_generation_performed: `{approved_artifact['label_generation_performed']}`",
        f"- feature_matrix_generation_performed: `{approved_artifact['feature_matrix_generation_performed']}`",
        f"- new_strategy_scoring_performed: `{approved_artifact['new_strategy_scoring_performed']}`",
        f"- trade_recommendations_generated: `{approved_artifact['trade_recommendations_generated']}`",
        f"- provider_requests_made_in_approval: `{approved_artifact['provider_requests_made_in_approval']}`",
        "",
        "## Predictive/Profitability Boundary",
        f"- predictive_usefulness: `{approved_artifact['predictive_usefulness']}`",
        f"- predictive_usefulness_acceptance_ready: `{approved_artifact['predictive_usefulness_acceptance_ready']}`",
        f"- profitability: `{approved_artifact['profitability']}`",
        f"- profitability_acceptance_ready: `{approved_artifact['profitability_acceptance_ready']}`",
        "",
        "## Runtime Boundary",
        f"- runtime_migration_recommended: `{approved_artifact['runtime_migration_recommended']}`",
        f"- runtime_migration_approved: `{approved_artifact['runtime_migration_approved']}`",
        f"- runtime_migration_active: `{approved_artifact['runtime_migration_active']}`",
        f"- runtime_use: `{approved_artifact['runtime_use']}`",
        f"- strategy_use: `{approved_artifact['strategy_use']}`",
        f"- paper_trading: `{approved_artifact['paper_trading']}`",
        f"- broker_execution: `{approved_artifact['broker_execution']}`",
        "",
        "## Approval Checklist Summary",
        f"- Total checks: `{summary['total_checks']}`",
        f"- Passed checks: `{summary['passed_checks']}`",
        f"- Failed checks: `{summary['failed_checks']}`",
        f"- Blocker count: `{summary['blocker_count']}`",
        "",
        "## Remaining Required Tasks",
    ]
    lines.extend(f"{index}. {task}" for index, task in enumerate(approved_artifact["remaining_roadmap"], start=1))
    lines.extend(
        [
            "",
            "## Guardrails",
            "- Created offline: `True`",
            "- Predictive experiment execution is authorized for a future research-only run only.",
            "- Predictive experiment executed: `False`",
            "- No labels, feature matrices, walk-forward validation, OOS evaluation, or strategy scoring were generated.",
            "- No Massive.com / Polygon provider data was fetched.",
            "- Runtime, Strategy, paper trading, and broker execution remain `NOT_AUTHORIZED`.",
            "- Predictive usefulness and profitability remain not accepted.",
            "",
        ]
    )
    return "\n".join(lines)


def write_predictive_experiment_execution_approved_v1(
    output_dir: str | Path,
    *,
    execution_candidate_review_package: dict[str, Any] | None = None,
    operator_attestation: dict[str, Any],
    filename: str | None = None,
) -> dict[str, Any]:
    """Write the predictive experiment execution approval JSON without overwriting output."""
    approved = build_predictive_experiment_execution_approved_v1(
        execution_candidate_review_package=execution_candidate_review_package,
        operator_attestation=operator_attestation,
    )
    validation = validate_predictive_experiment_execution_approved_v1(approved)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "predictive_experiment_execution_approved_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise PredictiveExperimentExecutionApprovalError(
            "predictive experiment execution approval filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise PredictiveExperimentExecutionApprovalError(
            "predictive experiment execution approval output already exists"
        )
    payload = canonical_json_bytes(approved)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": str(path),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
    }
