"""Offline approval ceremony for research-only applicability campaign execution."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import (
    research_applicability_campaign_execution_candidate_operator_review_service as candidate_review,
)


ARTIFACT_KIND_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_APPROVED = (
    "RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_APPROVED"
)
SCHEMA_VERSION_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_APPROVAL_V1 = (
    "research_applicability_campaign_execution_approval_v1"
)
RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_APPROVED = (
    "RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_APPROVED"
)
OPERATOR_DECISION_APPROVE_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION = (
    "APPROVE_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION"
)
OPERATOR_ATTESTATION_VERSION_V1 = (
    "research_applicability_campaign_execution_approval_operator_attestation_v1"
)
REQUIRED_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_APPROVAL_ATTESTATION_PHRASE = (
    "APPROVE RESEARCH APPLICABILITY CAMPAIGN EXECUTION AAPL SWING POSITION_SWING "
    "2022-01-01 2025-12-31 RESEARCH_ONLY_NON_ACTIONABLE"
)

EXPECTED_EXECUTION_CANDIDATE_DIGEST = (
    candidate_review.EXPECTED_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_CANDIDATE_DIGEST
)
EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    "9ab7e374c2cedd5b6dec8d674984cb6ddf44c18bf4c5abb744db54641c64ee60"
)
EXPECTED_REVIEW_CHECKLIST_TOTAL = len(candidate_review.REQUIRED_CHECK_IDS)
EXPECTED_REVIEW_CHECKLIST_PASSED = len(candidate_review.REQUIRED_CHECK_IDS)
EXPECTED_REVIEW_CHECKLIST_FAILED = 0
EXPECTED_REVIEW_BLOCKER_COUNT = 0

PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
INFO = "INFO"

OPERATOR_CONFIRMATION_FIELDS = [
    "operator_confirms_research_only_scope",
    "operator_confirms_aapl_only",
    "operator_confirms_profiles_swing_and_position_swing",
    "operator_confirms_no_provider_requests_in_approval",
    "operator_confirms_no_campaign_execution_performed",
    "operator_confirms_no_campaign_results_generated",
    "operator_confirms_no_runtime_migration_approval",
    "operator_confirms_no_runtime_activation",
    "operator_confirms_no_strategy_runtime_migration",
    "operator_confirms_no_paper_trading",
    "operator_confirms_no_broker_execution",
    "operator_confirms_no_predictive_usefulness",
    "operator_confirms_no_profitability_acceptance",
]

REMAINING_ROADMAP_AFTER_EXECUTION_APPROVAL = [
    "Research-only applicability campaign execution.",
    "Campaign result operator review.",
    "Predictive usefulness review.",
    "Profitability review.",
    "Separate runtime migration approval ceremony, if ever authorized.",
]

REQUIRED_APPROVAL_CHECK_IDS = [
    "execution_candidate_review_digest_matches_expected",
    "execution_candidate_review_has_zero_blockers",
    "execution_candidate_digest_matches_expected",
    "execution_request_id_matches",
    "campaign_plan_digest_matches",
    "campaign_plan_review_digest_matches",
    "dataset_availability_review_digest_matches",
    "swing_registry_approval_digest_matches",
    "position_swing_registry_approval_digest_matches",
    "campaign_scope_research_only",
    "ticker_universe_aapl_only",
    "profiles_swing_and_position_swing",
    "date_range_matches",
    "execution_mode_read_only_offline_research",
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
    "operator_campaign_plan_digest_confirmation_matches",
    "operator_campaign_plan_review_digest_confirmation_matches",
    "operator_dataset_availability_review_digest_confirmation_matches",
    "operator_swing_registry_approval_digest_confirmation_matches",
    "operator_position_swing_registry_approval_digest_confirmation_matches",
    "operator_confirms_research_only_scope",
    "operator_confirms_aapl_only",
    "operator_confirms_profiles_swing_and_position_swing",
    "operator_confirms_no_provider_requests_in_approval",
    "operator_confirms_no_campaign_execution_performed",
    "operator_confirms_no_campaign_results_generated",
    "operator_confirms_no_runtime_migration_approval",
    "operator_confirms_no_runtime_activation",
    "operator_confirms_no_strategy_runtime_migration",
    "operator_confirms_no_paper_trading",
    "operator_confirms_no_broker_execution",
    "operator_confirms_no_predictive_usefulness",
    "operator_confirms_no_profitability_acceptance",
    "campaign_execution_authorized_true",
    "campaign_execution_performed_false",
    "campaign_results_generated_false",
    "provider_requests_made_in_approval_false",
    "runtime_migration_approved_false",
    "runtime_migration_active_false",
    "strategy_runtime_migration_false",
    "runtime_use_not_authorized",
    "strategy_use_not_authorized",
    "paper_trading_not_authorized",
    "broker_execution_not_authorized",
    "automatic_stitching_false",
    "predictive_usefulness_not_accepted",
    "profitability_not_accepted",
]


class ResearchApplicabilityCampaignExecutionApprovalError(ValueError):
    """Raised when the research applicability campaign execution approval violates guardrails."""


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
        raise ResearchApplicabilityCampaignExecutionApprovalError(f"{field_name} mismatch")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise ResearchApplicabilityCampaignExecutionApprovalError(f"{field_name} must be false")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise ResearchApplicabilityCampaignExecutionApprovalError(f"{field_name} must be true")


def build_research_applicability_campaign_execution_approval_attestation_v1(
    *,
    operator_reference: str,
    operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str,
    operator_confirms_execution_candidate_digest: str,
    operator_confirms_execution_candidate_review_package_digest: str,
    operator_confirms_execution_request_id: str,
    operator_confirms_campaign_plan_digest: str,
    operator_confirms_campaign_plan_review_package_digest: str,
    operator_confirms_dataset_availability_review_digest: str,
    operator_confirms_swing_registry_approval_digest: str,
    operator_confirms_position_swing_registry_approval_digest: str,
    operator_confirms_research_only_scope: bool,
    operator_confirms_aapl_only: bool,
    operator_confirms_profiles_swing_and_position_swing: bool,
    operator_confirms_no_provider_requests_in_approval: bool,
    operator_confirms_no_campaign_execution_performed: bool,
    operator_confirms_no_campaign_results_generated: bool,
    operator_confirms_no_runtime_migration_approval: bool,
    operator_confirms_no_runtime_activation: bool,
    operator_confirms_no_strategy_runtime_migration: bool,
    operator_confirms_no_paper_trading: bool,
    operator_confirms_no_broker_execution: bool,
    operator_confirms_no_predictive_usefulness: bool,
    operator_confirms_no_profitability_acceptance: bool,
    operator_decision: str = OPERATOR_DECISION_APPROVE_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION,
    operator_attestation_version: str = OPERATOR_ATTESTATION_VERSION_V1,
) -> dict[str, Any]:
    """Build a non-secret operator attestation for research campaign execution approval."""
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
        "operator_confirms_campaign_plan_digest": operator_confirms_campaign_plan_digest,
        "operator_confirms_campaign_plan_review_package_digest": (
            operator_confirms_campaign_plan_review_package_digest
        ),
        "operator_confirms_dataset_availability_review_digest": (
            operator_confirms_dataset_availability_review_digest
        ),
        "operator_confirms_swing_registry_approval_digest": (
            operator_confirms_swing_registry_approval_digest
        ),
        "operator_confirms_position_swing_registry_approval_digest": (
            operator_confirms_position_swing_registry_approval_digest
        ),
        "operator_confirms_research_only_scope": operator_confirms_research_only_scope,
        "operator_confirms_aapl_only": operator_confirms_aapl_only,
        "operator_confirms_profiles_swing_and_position_swing": (
            operator_confirms_profiles_swing_and_position_swing
        ),
        "operator_confirms_no_provider_requests_in_approval": (
            operator_confirms_no_provider_requests_in_approval
        ),
        "operator_confirms_no_campaign_execution_performed": (
            operator_confirms_no_campaign_execution_performed
        ),
        "operator_confirms_no_campaign_results_generated": (
            operator_confirms_no_campaign_results_generated
        ),
        "operator_confirms_no_runtime_migration_approval": (
            operator_confirms_no_runtime_migration_approval
        ),
        "operator_confirms_no_runtime_activation": operator_confirms_no_runtime_activation,
        "operator_confirms_no_strategy_runtime_migration": (
            operator_confirms_no_strategy_runtime_migration
        ),
        "operator_confirms_no_paper_trading": operator_confirms_no_paper_trading,
        "operator_confirms_no_broker_execution": operator_confirms_no_broker_execution,
        "operator_confirms_no_predictive_usefulness": operator_confirms_no_predictive_usefulness,
        "operator_confirms_no_profitability_acceptance": (
            operator_confirms_no_profitability_acceptance
        ),
    }


def _source_review_package(review_package: dict[str, Any] | None) -> dict[str, Any]:
    source_review = (
        deepcopy(review_package)
        if review_package is not None
        else candidate_review.build_research_applicability_campaign_execution_candidate_review_package_v1()
    )
    try:
        validation = candidate_review.validate_research_applicability_campaign_execution_candidate_review_package_v1(
            source_review
        )
    except candidate_review.ResearchApplicabilityCampaignExecutionCandidateOperatorReviewError as exc:
        raise ResearchApplicabilityCampaignExecutionApprovalError(
            f"source execution candidate review package invalid: {exc}"
        ) from exc
    _expect(
        validation["research_applicability_campaign_execution_candidate_review_package_digest"],
        EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "source execution candidate review package digest",
    )
    _expect(validation["failed_checks"], 0, "source execution candidate review failed check count")
    _expect(validation["blocker_count"], 0, "source execution candidate review blocker count")
    return source_review


def _review_evidence(source_review: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_execution_candidate_kind": source_review["reviewed_execution_candidate_kind"],
        "source_execution_candidate_status": source_review["reviewed_execution_candidate_status"],
        "source_execution_candidate_digest": source_review["reviewed_execution_candidate_digest"],
        "source_execution_candidate_review_package_kind": source_review["artifact_kind"],
        "source_execution_candidate_review_status": source_review["review_status"],
        "source_execution_candidate_review_package_digest": source_review[
            "research_applicability_campaign_execution_candidate_review_package_digest"
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
        "campaign_execution_request_id": source_review["reviewed_execution_request_id"],
        "campaign_scope": source_review["campaign_scope"],
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
        "research_campaign_plan_digest": source_review["research_campaign_plan_digest"],
        "research_campaign_plan_review_package_digest": (
            source_review["research_campaign_plan_review_package_digest"]
        ),
        "dataset_file_availability_verification_review_package_digest": source_review[
            "dataset_file_availability_verification_review_package_digest"
        ],
        "read_only_discovery_review_package_digest": source_review[
            "read_only_discovery_review_package_digest"
        ],
        "runtime_migration_review_package_digest": source_review[
            "runtime_migration_review_package_digest"
        ],
        "swing_registry_approval_digest": source_review["swing_registry_approval_digest"],
        "position_swing_registry_approval_digest": source_review[
            "position_swing_registry_approval_digest"
        ],
    }


def _attestation_checks(attestation: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not isinstance(attestation, dict):
        return [
            _check("operator_decision_approved", OPERATOR_DECISION_APPROVE_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION, None),
            _check("operator_attestation_phrase_matches", REQUIRED_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_APPROVAL_ATTESTATION_PHRASE, None),
            _check("operator_execution_candidate_digest_confirmation_matches", EXPECTED_EXECUTION_CANDIDATE_DIGEST, None),
            _check("operator_execution_candidate_review_digest_confirmation_matches", EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST, None),
            _check("operator_execution_request_id_confirmation_matches", candidate_review.execution_candidate.CAMPAIGN_EXECUTION_REQUEST_ID, None),
            _check("operator_campaign_plan_digest_confirmation_matches", candidate_review.execution_candidate.EXPECTED_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_DIGEST, None),
            _check("operator_campaign_plan_review_digest_confirmation_matches", candidate_review.execution_candidate.EXPECTED_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_REVIEW_PACKAGE_DIGEST, None),
            _check("operator_dataset_availability_review_digest_confirmation_matches", candidate_review.execution_candidate.EXPECTED_DATASET_FILE_AVAILABILITY_VERIFICATION_REVIEW_PACKAGE_DIGEST, None),
            _check("operator_swing_registry_approval_digest_confirmation_matches", candidate_review.execution_candidate.plan_review.campaign_plan.availability_review.verification.discovery.runtime_planning.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST, None),
            _check("operator_position_swing_registry_approval_digest_confirmation_matches", candidate_review.execution_candidate.plan_review.campaign_plan.availability_review.verification.discovery.runtime_planning.EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST, None),
            *[_check(field, True, None) for field in OPERATOR_CONFIRMATION_FIELDS],
        ]
    return [
        _check("operator_decision_approved", OPERATOR_DECISION_APPROVE_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION, attestation.get("operator_decision")),
        _check("operator_attestation_phrase_matches", REQUIRED_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_APPROVAL_ATTESTATION_PHRASE, attestation.get("operator_attestation_phrase")),
        _check("operator_execution_candidate_digest_confirmation_matches", EXPECTED_EXECUTION_CANDIDATE_DIGEST, attestation.get("operator_confirms_execution_candidate_digest")),
        _check("operator_execution_candidate_review_digest_confirmation_matches", EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST, attestation.get("operator_confirms_execution_candidate_review_package_digest")),
        _check("operator_execution_request_id_confirmation_matches", candidate_review.execution_candidate.CAMPAIGN_EXECUTION_REQUEST_ID, attestation.get("operator_confirms_execution_request_id")),
        _check("operator_campaign_plan_digest_confirmation_matches", candidate_review.execution_candidate.EXPECTED_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_DIGEST, attestation.get("operator_confirms_campaign_plan_digest")),
        _check("operator_campaign_plan_review_digest_confirmation_matches", candidate_review.execution_candidate.EXPECTED_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_REVIEW_PACKAGE_DIGEST, attestation.get("operator_confirms_campaign_plan_review_package_digest")),
        _check("operator_dataset_availability_review_digest_confirmation_matches", candidate_review.execution_candidate.EXPECTED_DATASET_FILE_AVAILABILITY_VERIFICATION_REVIEW_PACKAGE_DIGEST, attestation.get("operator_confirms_dataset_availability_review_digest")),
        _check("operator_swing_registry_approval_digest_confirmation_matches", candidate_review.execution_candidate.plan_review.campaign_plan.availability_review.verification.discovery.runtime_planning.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST, attestation.get("operator_confirms_swing_registry_approval_digest")),
        _check("operator_position_swing_registry_approval_digest_confirmation_matches", candidate_review.execution_candidate.plan_review.campaign_plan.availability_review.verification.discovery.runtime_planning.EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST, attestation.get("operator_confirms_position_swing_registry_approval_digest")),
        *[_check(field, True, attestation.get(field)) for field in OPERATOR_CONFIRMATION_FIELDS],
    ]


def _validated_operator_attestation(attestation: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(attestation, dict):
        raise ResearchApplicabilityCampaignExecutionApprovalError(
            "operator_attestation must be a JSON object"
        )
    for field in (
        "operator_reference",
        "operator_attestation_timestamp_utc",
        "operator_attestation_version",
    ):
        value = attestation.get(field)
        if not isinstance(value, str) or not value.strip():
            raise ResearchApplicabilityCampaignExecutionApprovalError(
                f"{field} must be a non-empty string"
            )
    failed = [item for item in _attestation_checks(attestation) if item["status"] != PASS]
    if failed:
        raise ResearchApplicabilityCampaignExecutionApprovalError(
            f"operator attestation failed: {failed[0]['check_id']}"
        )
    return deepcopy(attestation)


def _planned_outputs_not_generated(outputs: Any) -> bool:
    return isinstance(outputs, list) and bool(outputs) and all(
        isinstance(output, dict)
        and output.get("status") == candidate_review.execution_candidate.PLANNED_NOT_GENERATED
        and output.get("generated") is False
        for output in outputs
    )


def _planned_outputs_research_only(outputs: Any) -> bool:
    return isinstance(outputs, list) and bool(outputs) and all(
        isinstance(output, dict)
        and output.get("output_label") == candidate_review.execution_candidate.RESEARCH_ONLY_NON_ACTIONABLE
        for output in outputs
    )


def _approval_checklist(approved: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        _check("execution_candidate_review_digest_matches_expected", EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST, approved.get("source_execution_candidate_review_package_digest")),
        _check("execution_candidate_review_has_zero_blockers", EXPECTED_REVIEW_BLOCKER_COUNT, approved.get("source_execution_candidate_review_blocker_count")),
        _check("execution_candidate_digest_matches_expected", EXPECTED_EXECUTION_CANDIDATE_DIGEST, approved.get("source_execution_candidate_digest")),
        _check("execution_request_id_matches", candidate_review.execution_candidate.CAMPAIGN_EXECUTION_REQUEST_ID, approved.get("campaign_execution_request_id")),
        _check("campaign_plan_digest_matches", candidate_review.execution_candidate.EXPECTED_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_DIGEST, approved.get("research_campaign_plan_digest")),
        _check("campaign_plan_review_digest_matches", candidate_review.execution_candidate.EXPECTED_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_REVIEW_PACKAGE_DIGEST, approved.get("research_campaign_plan_review_package_digest")),
        _check("dataset_availability_review_digest_matches", candidate_review.execution_candidate.EXPECTED_DATASET_FILE_AVAILABILITY_VERIFICATION_REVIEW_PACKAGE_DIGEST, approved.get("dataset_file_availability_verification_review_package_digest")),
        _check("swing_registry_approval_digest_matches", candidate_review.execution_candidate.plan_review.campaign_plan.availability_review.verification.discovery.runtime_planning.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST, approved.get("swing_registry_approval_digest")),
        _check("position_swing_registry_approval_digest_matches", candidate_review.execution_candidate.plan_review.campaign_plan.availability_review.verification.discovery.runtime_planning.EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST, approved.get("position_swing_registry_approval_digest")),
        _check("campaign_scope_research_only", "RESEARCH_ONLY", approved.get("campaign_scope")),
        _check("ticker_universe_aapl_only", ["AAPL"], approved.get("ticker_universe")),
        _check("profiles_swing_and_position_swing", ["POSITION_SWING", "SWING"], sorted(approved.get("dataset_profiles") or [])),
        _check("date_range_matches", {"start": candidate_review.execution_candidate.DATE_RANGE_START, "end": candidate_review.execution_candidate.DATE_RANGE_END}, {"start": approved.get("date_range_start"), "end": approved.get("date_range_end")}),
        _check("execution_mode_read_only_offline_research", candidate_review.execution_candidate.READ_ONLY_OFFLINE_RESEARCH, approved.get("execution_mode")),
        _check("runtime_mode_not_runtime", candidate_review.execution_candidate.NOT_RUNTIME, approved.get("runtime_mode")),
        _check("strategy_mode_not_strategy_input", candidate_review.execution_candidate.NOT_STRATEGY_INPUT, approved.get("strategy_mode")),
        _check("broker_mode_disabled", candidate_review.execution_candidate.DISABLED, approved.get("broker_mode")),
        _check("paper_trading_mode_disabled", candidate_review.execution_candidate.DISABLED, approved.get("paper_trading_mode")),
        _check("planned_outputs_not_generated", True, _planned_outputs_not_generated(approved.get("planned_outputs"))),
        _check("planned_outputs_research_only_non_actionable", True, _planned_outputs_research_only(approved.get("planned_outputs"))),
        *_attestation_checks(approved.get("operator_attestation") if isinstance(approved.get("operator_attestation"), dict) else None),
        _check("campaign_execution_authorized_true", True, approved.get("campaign_execution_authorized")),
        _check("campaign_execution_performed_false", False, approved.get("campaign_execution_performed")),
        _check("campaign_results_generated_false", False, approved.get("campaign_results_generated")),
        _check("provider_requests_made_in_approval_false", False, approved.get("provider_requests_made_in_approval")),
        _check("runtime_migration_approved_false", False, approved.get("runtime_migration_approved")),
        _check("runtime_migration_active_false", False, approved.get("runtime_migration_active")),
        _check("strategy_runtime_migration_false", False, approved.get("strategy_runtime_migration")),
        _check("runtime_use_not_authorized", candidate_review.execution_candidate.NOT_AUTHORIZED, approved.get("runtime_use")),
        _check("strategy_use_not_authorized", candidate_review.execution_candidate.NOT_AUTHORIZED, approved.get("strategy_use")),
        _check("paper_trading_not_authorized", candidate_review.execution_candidate.NOT_AUTHORIZED, approved.get("paper_trading")),
        _check("broker_execution_not_authorized", candidate_review.execution_candidate.NOT_AUTHORIZED, approved.get("broker_execution")),
        _check("automatic_stitching_false", False, approved.get("automatic_stitching")),
        _check("predictive_usefulness_not_accepted", acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED, approved.get("predictive_usefulness"), severity=INFO),
        _check("profitability_not_accepted", acquisition.PROFITABILITY_NOT_ACCEPTED, approved.get("profitability"), severity=INFO),
    ]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(checklist)
    passed = sum(1 for item in checklist if item["status"] == PASS)
    failed = total - passed
    blocker_count = sum(1 for item in checklist if item["status"] == FAIL and item["severity"] == BLOCKER)
    return {
        "total_checks": total,
        "passed_checks": passed,
        "failed_checks": failed,
        "blocker_count": blocker_count,
        "campaign_execution_authorized_by_operator": failed == 0,
        "campaign_execution_performed": False,
        "software_runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
        "software_predictive_usefulness_authorized": False,
        "software_profitability_authorized": False,
    }


def _digest_payload(approved_artifact: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(approved_artifact)
    payload.pop("research_applicability_campaign_execution_approval_digest", None)
    return payload


def research_applicability_campaign_execution_approval_digest_v1(
    approved_artifact: dict[str, Any],
) -> str:
    """Return the deterministic semantic digest for an execution approval artifact."""
    return semantic_digest(_digest_payload(approved_artifact))


def build_research_applicability_campaign_execution_approved_v1(
    *,
    execution_candidate_review_package: dict[str, Any] | None = None,
    operator_attestation: dict[str, Any],
) -> dict[str, Any]:
    """Build an offline approval artifact that authorizes only future research execution."""
    source_review = _source_review_package(execution_candidate_review_package)
    attestation = _validated_operator_attestation(operator_attestation)
    approved = {
        "artifact_kind": ARTIFACT_KIND_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_APPROVED,
        "schema_version": SCHEMA_VERSION_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_APPROVAL_V1,
        "approval_status": RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_APPROVED,
        "campaign_execution_authorized": True,
        "campaign_execution_performed": False,
        "campaign_results_generated": False,
        "research_only": True,
        "created_offline": True,
        "provider_requests_made_in_approval": False,
        "runtime_migration_approved": False,
        "runtime_migration_active": False,
        "strategy_runtime_migration": False,
        "runtime_use": candidate_review.execution_candidate.NOT_AUTHORIZED,
        "strategy_use": candidate_review.execution_candidate.NOT_AUTHORIZED,
        "paper_trading": candidate_review.execution_candidate.NOT_AUTHORIZED,
        "broker_execution": candidate_review.execution_candidate.NOT_AUTHORIZED,
        "automatic_stitching": False,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "operator_attestation": attestation,
        "remaining_roadmap": list(REMAINING_ROADMAP_AFTER_EXECUTION_APPROVAL),
        **_review_evidence(source_review),
    }
    checklist = _approval_checklist(approved)
    approved["approval_checklist"] = checklist
    approved["approval_summary"] = _summary(checklist)
    approved["research_applicability_campaign_execution_approval_digest"] = (
        research_applicability_campaign_execution_approval_digest_v1(approved)
    )
    validate_research_applicability_campaign_execution_approved_v1(approved)
    return approved


def _reject_forbidden_values(mapping: dict[str, Any], *, path: str = "approved_artifact") -> None:
    for key, value in mapping.items():
        current_path = f"{path}.{key}"
        if isinstance(value, str) and value in {
            "RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTED",
            "RESEARCH_APPLICABILITY_CAMPAIGN_RESULTS",
            "PREDICTIVE_USEFULNESS_ACCEPTED",
            "PROFITABILITY_ACCEPTED",
            "RUNTIME_MIGRATION_APPROVED",
            "RUNTIME_MIGRATION_ACTIVE",
            "STRATEGY_RUNTIME_MIGRATION",
        }:
            raise ResearchApplicabilityCampaignExecutionApprovalError(
                f"{current_path} must not emit {value}"
            )
        if key in {
            "campaign_execution_performed",
            "campaign_results_generated",
            "runtime_migration_approved",
            "runtime_migration_active",
            "strategy_runtime_migration",
            "automatic_stitching",
            "provider_requests_made_in_approval",
            "generated",
            "execution_performed",
            "output_generated",
        } and value is True:
            raise ResearchApplicabilityCampaignExecutionApprovalError(f"{current_path} must be false")
        if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and value == "AUTHORIZED":
            raise ResearchApplicabilityCampaignExecutionApprovalError(
                f"{current_path} must not be AUTHORIZED"
            )
        if key in {"predictive_usefulness", "profitability"} and value == "accepted":
            raise ResearchApplicabilityCampaignExecutionApprovalError(
                f"{current_path} must not be accepted"
            )
        if isinstance(value, dict):
            _reject_forbidden_values(value, path=current_path)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, dict):
                    _reject_forbidden_values(item, path=f"{current_path}[{index}]")


def validate_research_applicability_campaign_execution_approved_v1(
    approved_artifact: dict[str, Any],
) -> dict[str, Any]:
    """Validate approval while preserving all non-execution and runtime guardrails."""
    if not isinstance(approved_artifact, dict):
        raise ResearchApplicabilityCampaignExecutionApprovalError(
            "approved artifact must be a JSON object"
        )
    _reject_forbidden_values(approved_artifact)
    _expect(
        approved_artifact.get("artifact_kind"),
        ARTIFACT_KIND_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_APPROVED,
        "artifact_kind",
    )
    _expect(
        approved_artifact.get("schema_version"),
        SCHEMA_VERSION_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_APPROVAL_V1,
        "schema_version",
    )
    _expect(
        approved_artifact.get("approval_status"),
        RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_APPROVED,
        "approval_status",
    )
    for field in ("campaign_execution_authorized", "research_only", "created_offline"):
        _expect_true(approved_artifact.get(field), field)
    for field in (
        "campaign_execution_performed",
        "campaign_results_generated",
        "provider_requests_made_in_approval",
        "runtime_migration_approved",
        "runtime_migration_active",
        "strategy_runtime_migration",
        "automatic_stitching",
    ):
        _expect_false(approved_artifact.get(field), field)
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(approved_artifact.get(field), candidate_review.execution_candidate.NOT_AUTHORIZED, field)
    _expect(
        approved_artifact.get("predictive_usefulness"),
        acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "predictive_usefulness",
    )
    _expect(approved_artifact.get("profitability"), acquisition.PROFITABILITY_NOT_ACCEPTED, "profitability")
    for field, expected in {
        "source_execution_candidate_kind": candidate_review.execution_candidate.ARTIFACT_KIND_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_CANDIDATE,
        "source_execution_candidate_status": candidate_review.execution_candidate.RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_READY_FOR_OPERATOR_REVIEW,
        "source_execution_candidate_digest": EXPECTED_EXECUTION_CANDIDATE_DIGEST,
        "source_execution_candidate_review_package_kind": candidate_review.ARTIFACT_KIND_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_CANDIDATE_REVIEW_PACKAGE,
        "source_execution_candidate_review_status": candidate_review.RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_CANDIDATE_REVIEW_PACKAGE_READY,
        "source_execution_candidate_review_package_digest": EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "source_execution_candidate_review_checklist_total": EXPECTED_REVIEW_CHECKLIST_TOTAL,
        "source_execution_candidate_review_checklist_passed": EXPECTED_REVIEW_CHECKLIST_PASSED,
        "source_execution_candidate_review_checklist_failed": EXPECTED_REVIEW_CHECKLIST_FAILED,
        "source_execution_candidate_review_blocker_count": EXPECTED_REVIEW_BLOCKER_COUNT,
        "campaign_execution_request_id": candidate_review.execution_candidate.CAMPAIGN_EXECUTION_REQUEST_ID,
        "campaign_scope": "RESEARCH_ONLY",
        "ticker_universe": ["AAPL"],
        "dataset_profiles": ["SWING", "POSITION_SWING"],
        "date_range_start": candidate_review.execution_candidate.DATE_RANGE_START,
        "date_range_end": candidate_review.execution_candidate.DATE_RANGE_END,
        "execution_mode": candidate_review.execution_candidate.READ_ONLY_OFFLINE_RESEARCH,
        "runtime_mode": candidate_review.execution_candidate.NOT_RUNTIME,
        "strategy_mode": candidate_review.execution_candidate.NOT_STRATEGY_INPUT,
        "broker_mode": candidate_review.execution_candidate.DISABLED,
        "paper_trading_mode": candidate_review.execution_candidate.DISABLED,
        "planned_output_count": len(candidate_review.execution_candidate.PLANNED_OUTPUT_NAMES),
        "planned_outputs_status": candidate_review.execution_candidate.PLANNED_NOT_GENERATED,
        "planned_outputs_label": candidate_review.execution_candidate.RESEARCH_ONLY_NON_ACTIONABLE,
        "research_campaign_plan_digest": candidate_review.execution_candidate.EXPECTED_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_DIGEST,
        "research_campaign_plan_review_package_digest": candidate_review.execution_candidate.EXPECTED_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_REVIEW_PACKAGE_DIGEST,
        "dataset_file_availability_verification_review_package_digest": candidate_review.execution_candidate.EXPECTED_DATASET_FILE_AVAILABILITY_VERIFICATION_REVIEW_PACKAGE_DIGEST,
        "read_only_discovery_review_package_digest": candidate_review.execution_candidate.EXPECTED_READ_ONLY_DISCOVERY_REVIEW_PACKAGE_DIGEST,
        "runtime_migration_review_package_digest": candidate_review.execution_candidate.EXPECTED_RUNTIME_MIGRATION_REVIEW_PACKAGE_DIGEST,
        "swing_registry_approval_digest": candidate_review.execution_candidate.plan_review.campaign_plan.availability_review.verification.discovery.runtime_planning.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST,
        "position_swing_registry_approval_digest": candidate_review.execution_candidate.plan_review.campaign_plan.availability_review.verification.discovery.runtime_planning.EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST,
        "remaining_roadmap": REMAINING_ROADMAP_AFTER_EXECUTION_APPROVAL,
    }.items():
        _expect(approved_artifact.get(field), expected, field)
    _validated_operator_attestation(approved_artifact.get("operator_attestation"))
    checklist = _approval_checklist(approved_artifact)
    _expect([item["check_id"] for item in checklist], REQUIRED_APPROVAL_CHECK_IDS, "approval_checklist check IDs")
    failed = [item for item in checklist if item["status"] != PASS]
    if failed:
        raise ResearchApplicabilityCampaignExecutionApprovalError(
            f"approval checklist contains failed check: {failed[0]['check_id']}"
        )
    _expect(approved_artifact.get("approval_checklist"), checklist, "approval_checklist")
    summary = _summary(checklist)
    _expect(approved_artifact.get("approval_summary"), summary, "approval_summary")
    _expect_true(
        summary.get("campaign_execution_authorized_by_operator"),
        "campaign_execution_authorized_by_operator",
    )
    _expect_false(summary.get("campaign_execution_performed"), "campaign_execution_performed")
    _expect_false(summary.get("software_runtime_migration_authorized"), "software_runtime_migration_authorized")
    _expect_false(summary.get("software_runtime_activation_authorized"), "software_runtime_activation_authorized")
    _expect_false(
        summary.get("software_predictive_usefulness_authorized"),
        "software_predictive_usefulness_authorized",
    )
    _expect_false(summary.get("software_profitability_authorized"), "software_profitability_authorized")
    digest = approved_artifact.get("research_applicability_campaign_execution_approval_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise ResearchApplicabilityCampaignExecutionApprovalError(
            "research_applicability_campaign_execution_approval_digest missing"
        )
    _expect(
        digest,
        research_applicability_campaign_execution_approval_digest_v1(approved_artifact),
        "research_applicability_campaign_execution_approval_digest",
    )
    return {
        "status": "RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_APPROVED_VALID",
        "artifact_kind": approved_artifact["artifact_kind"],
        "approval_status": approved_artifact["approval_status"],
        "research_applicability_campaign_execution_approval_digest": digest,
        "campaign_execution_request_id": candidate_review.execution_candidate.CAMPAIGN_EXECUTION_REQUEST_ID,
        "source_execution_candidate_digest": EXPECTED_EXECUTION_CANDIDATE_DIGEST,
        "source_execution_candidate_review_package_digest": EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "research_campaign_plan_digest": candidate_review.execution_candidate.EXPECTED_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_DIGEST,
        "research_campaign_plan_review_package_digest": candidate_review.execution_candidate.EXPECTED_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_REVIEW_PACKAGE_DIGEST,
        "dataset_file_availability_verification_review_package_digest": candidate_review.execution_candidate.EXPECTED_DATASET_FILE_AVAILABILITY_VERIFICATION_REVIEW_PACKAGE_DIGEST,
        "swing_registry_approval_digest": approved_artifact["swing_registry_approval_digest"],
        "position_swing_registry_approval_digest": approved_artifact[
            "position_swing_registry_approval_digest"
        ],
        "campaign_execution_authorized": True,
        "campaign_execution_performed": False,
        "campaign_results_generated": False,
        "runtime_migration_approved": False,
        "runtime_migration_active": False,
        "strategy_runtime_migration": False,
        "runtime_use": candidate_review.execution_candidate.NOT_AUTHORIZED,
        "strategy_use": candidate_review.execution_candidate.NOT_AUTHORIZED,
        "paper_trading": candidate_review.execution_candidate.NOT_AUTHORIZED,
        "broker_execution": candidate_review.execution_candidate.NOT_AUTHORIZED,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "total_checks": summary["total_checks"],
        "passed_checks": summary["passed_checks"],
        "failed_checks": summary["failed_checks"],
        "blocker_count": summary["blocker_count"],
    }


def build_research_applicability_campaign_execution_approved_markdown_v1(
    approved_artifact: dict[str, Any],
) -> str:
    """Render a sanitized research applicability campaign execution approval status document."""
    validation = validate_research_applicability_campaign_execution_approved_v1(approved_artifact)
    attestation = approved_artifact["operator_attestation"]
    summary = approved_artifact["approval_summary"]
    lines = [
        "# MarketFlow Research Applicability Campaign Execution Approval Status",
        "",
        "## Title",
        "- Research-Only Applicability Campaign Execution Approval Ceremony v1.",
        "",
        "## Approved Research Campaign Execution",
        f"- Artifact kind: `{approved_artifact['artifact_kind']}`",
        f"- Approval status: `{approved_artifact['approval_status']}`",
        f"- Campaign execution request ID: `{approved_artifact['campaign_execution_request_id']}`",
        f"- Campaign execution authorized: `{approved_artifact['campaign_execution_authorized']}`",
        f"- Campaign execution performed: `{approved_artifact['campaign_execution_performed']}`",
        f"- Campaign results generated: `{approved_artifact['campaign_results_generated']}`",
        f"- Approval digest: `{validation['research_applicability_campaign_execution_approval_digest']}`",
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
        "## Campaign Scope",
        f"- Campaign scope: `{approved_artifact['campaign_scope']}`",
        f"- Ticker universe: `{', '.join(approved_artifact['ticker_universe'])}`",
        f"- Dataset profiles: `{', '.join(approved_artifact['dataset_profiles'])}`",
        f"- Date range: `{approved_artifact['date_range_start']}` through `{approved_artifact['date_range_end']}`",
        f"- Execution mode: `{approved_artifact['execution_mode']}`",
        "",
        "## Execution Boundary",
        f"- campaign_execution_authorized: `{approved_artifact['campaign_execution_authorized']}`",
        f"- campaign_execution_performed: `{approved_artifact['campaign_execution_performed']}`",
        f"- campaign_results_generated: `{approved_artifact['campaign_results_generated']}`",
        f"- provider_requests_made_in_approval: `{approved_artifact['provider_requests_made_in_approval']}`",
        "",
        "## Runtime Boundary",
        f"- runtime_migration_approved: `{approved_artifact['runtime_migration_approved']}`",
        f"- runtime_migration_active: `{approved_artifact['runtime_migration_active']}`",
        f"- strategy_runtime_migration: `{approved_artifact['strategy_runtime_migration']}`",
        f"- runtime_use: `{approved_artifact['runtime_use']}`",
        f"- strategy_use: `{approved_artifact['strategy_use']}`",
        f"- paper_trading: `{approved_artifact['paper_trading']}`",
        f"- broker_execution: `{approved_artifact['broker_execution']}`",
        f"- predictive_usefulness: `{approved_artifact['predictive_usefulness']}`",
        f"- profitability: `{approved_artifact['profitability']}`",
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
            "- Campaign execution is authorized for a future research-only run only.",
            "- Campaign execution performed: `False`",
            "- Campaign results generated: `False`",
            "- No Massive.com / Polygon provider data was fetched.",
            "- No walk-forward validation or strategy scoring was run.",
            "- Runtime, Strategy, paper trading, and broker execution use remain `NOT_AUTHORIZED`.",
            "- Predictive usefulness and profitability remain not accepted.",
            "",
        ]
    )
    return "\n".join(lines)


def write_research_applicability_campaign_execution_approved_v1(
    output_dir: str | Path,
    *,
    execution_candidate_review_package: dict[str, Any] | None = None,
    operator_attestation: dict[str, Any],
    filename: str | None = None,
) -> dict[str, Any]:
    """Write the campaign execution approval JSON artifact without overwriting output."""
    approved = build_research_applicability_campaign_execution_approved_v1(
        execution_candidate_review_package=execution_candidate_review_package,
        operator_attestation=operator_attestation,
    )
    validation = validate_research_applicability_campaign_execution_approved_v1(approved)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "research_applicability_campaign_execution_approved_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise ResearchApplicabilityCampaignExecutionApprovalError(
            "research applicability campaign execution approval filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise ResearchApplicabilityCampaignExecutionApprovalError(
            "research applicability campaign execution approval output already exists"
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
