"""Offline operator-review package for research applicability campaign execution candidates."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import research_applicability_campaign_execution_candidate_service as execution_candidate


ARTIFACT_KIND_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_CANDIDATE_REVIEW_PACKAGE = (
    "RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_CANDIDATE_REVIEW_PACKAGE"
)
SCHEMA_VERSION_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_CANDIDATE_REVIEW_V1 = (
    "research_applicability_campaign_execution_candidate_review_v1"
)
RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_CANDIDATE_REVIEW_PACKAGE_READY = (
    "RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_CANDIDATE_REVIEW_PACKAGE_READY"
)
RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_CANDIDATE_STATUS_BINDING = (
    "RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_CANDIDATE_STATUS_BINDING"
)
RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_CANDIDATE_OBJECT_BINDING = (
    "RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_CANDIDATE_OBJECT_BINDING"
)

EXPECTED_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_CANDIDATE_DIGEST = (
    "d5d19a5b32b55b24f00568e021790c082a39f147618032702d2ecdcec62c0b27"
)
EXPECTED_CANDIDATE_CHECKLIST_TOTAL = len(execution_candidate.REQUIRED_CHECK_IDS)
EXPECTED_CANDIDATE_CHECKLIST_PASSED = len(execution_candidate.REQUIRED_CHECK_IDS)
EXPECTED_CANDIDATE_CHECKLIST_FAILED = 0
EXPECTED_CANDIDATE_BLOCKER_COUNT = 0

PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
INFO = "INFO"

REQUIRED_CHECK_IDS = [
    "execution_candidate_kind_matches",
    "execution_candidate_status_ready_for_review",
    "execution_candidate_digest_matches",
    "execution_request_id_matches",
    "execution_candidate_checklist_zero_blockers",
    "campaign_plan_digest_bound",
    "campaign_plan_review_digest_bound",
    "dataset_availability_review_digest_bound",
    "read_only_discovery_review_digest_bound",
    "runtime_migration_review_digest_bound",
    "swing_registry_approval_digest_bound",
    "position_swing_registry_approval_digest_bound",
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
    "execution_gates_defined",
    "risk_controls_defined",
    "campaign_execution_authorized_false",
    "campaign_execution_performed_false",
    "campaign_results_generated_false",
    "provider_requests_made_in_review_false",
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
    "no_campaign_execution_artifact_created",
]

REMAINING_REQUIRED_TASKS = [
    "Research-only applicability campaign execution approval ceremony.",
    "Research-only applicability campaign execution, if approved.",
    "Campaign result operator review.",
    "Predictive usefulness review.",
    "Profitability review.",
    "Separate runtime migration approval ceremony, if ever authorized.",
]

FORBIDDEN_APPROVAL_FIELDS = frozenset(
    {
        "operator_approved_by",
        "operator_approval_timestamp",
        "operator_approval_digest",
        "operator_signature",
        "approval_status",
    }
)


class ResearchApplicabilityCampaignExecutionCandidateOperatorReviewError(ValueError):
    """Raised when a research applicability execution candidate review package violates guardrails."""


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
        raise ResearchApplicabilityCampaignExecutionCandidateOperatorReviewError(
            f"{field_name} mismatch"
        )


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise ResearchApplicabilityCampaignExecutionCandidateOperatorReviewError(
            f"{field_name} must be false"
        )


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise ResearchApplicabilityCampaignExecutionCandidateOperatorReviewError(
            f"{field_name} must be true"
        )


def _review_context() -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_CANDIDATE_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_CANDIDATE_REVIEW_V1,
        "review_status": RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_CANDIDATE_REVIEW_PACKAGE_READY,
        "operator_decision_required": True,
        "operator_decision": None,
        "operator_approved_by": None,
        "operator_approval_timestamp": None,
        "operator_approval_digest": None,
        "operator_signature": None,
        "approval_status": None,
        "campaign_execution_authorized": False,
        "campaign_execution_performed": False,
        "campaign_results_generated": False,
        "campaign_execution_artifact_created": False,
        "runtime_migration_approved": False,
        "runtime_migration_active": False,
        "strategy_runtime_migration": False,
        "runtime_use": execution_candidate.NOT_AUTHORIZED,
        "strategy_use": execution_candidate.NOT_AUTHORIZED,
        "paper_trading": execution_candidate.NOT_AUTHORIZED,
        "broker_execution": execution_candidate.NOT_AUTHORIZED,
        "automatic_stitching": False,
        "created_offline": True,
        "provider_requests_made_in_review": False,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "software_campaign_execution_authorized": False,
        "software_runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def _candidate_evidence_from_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    try:
        validation = execution_candidate.validate_research_applicability_campaign_execution_candidate_v1(candidate)
    except execution_candidate.ResearchApplicabilityCampaignExecutionCandidateError as exc:
        raise ResearchApplicabilityCampaignExecutionCandidateOperatorReviewError(
            f"source research applicability campaign execution candidate invalid: {exc}"
        ) from exc
    _expect(
        validation["research_applicability_campaign_execution_candidate_digest"],
        EXPECTED_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_CANDIDATE_DIGEST,
        "research_applicability_campaign_execution_candidate_digest",
    )
    return {
        "reviewed_execution_candidate_kind": candidate["artifact_kind"],
        "reviewed_execution_candidate_status": candidate["candidate_status"],
        "reviewed_execution_candidate_digest": validation[
            "research_applicability_campaign_execution_candidate_digest"
        ],
        "reviewed_execution_request_id": candidate["campaign_execution_request_id"],
        "reviewed_candidate_checklist_total": validation["total_checks"],
        "reviewed_candidate_checklist_passed": validation["passed_checks"],
        "reviewed_candidate_checklist_failed": validation["failed_checks"],
        "reviewed_candidate_blocker_count": validation["blocker_count"],
        "campaign_scope": candidate["campaign_scope"],
        "ticker_universe": list(candidate["ticker_universe"]),
        "dataset_profiles": list(candidate["dataset_profiles"]),
        "date_range_start": candidate["date_range_start"],
        "date_range_end": candidate["date_range_end"],
        "execution_mode": candidate["execution_mode"],
        "runtime_mode": candidate["runtime_mode"],
        "strategy_mode": candidate["strategy_mode"],
        "broker_mode": candidate["broker_mode"],
        "paper_trading_mode": candidate["paper_trading_mode"],
        "planned_output_count": len(candidate["planned_outputs"]),
        "planned_outputs_status": execution_candidate.PLANNED_NOT_GENERATED,
        "planned_outputs_label": execution_candidate.RESEARCH_ONLY_NON_ACTIONABLE,
        "planned_inputs": deepcopy(candidate["planned_inputs"]),
        "planned_outputs": deepcopy(candidate["planned_outputs"]),
        "execution_gates": list(candidate["execution_gates"]),
        "risk_controls": list(candidate["risk_controls"]),
        "research_campaign_plan_digest": candidate["research_campaign_plan_digest"],
        "research_campaign_plan_review_package_digest": (
            candidate["research_campaign_plan_review_package_digest"]
        ),
        "dataset_file_availability_verification_review_package_digest": candidate[
            "dataset_file_availability_verification_review_package_digest"
        ],
        "read_only_discovery_review_package_digest": candidate[
            "read_only_discovery_review_package_digest"
        ],
        "runtime_migration_review_package_digest": candidate[
            "runtime_migration_review_package_digest"
        ],
        "swing_registry_approval_digest": candidate["swing_registry_approval_digest"],
        "position_swing_registry_approval_digest": candidate[
            "position_swing_registry_approval_digest"
        ],
    }


def _recorded_candidate_evidence() -> dict[str, Any]:
    return _candidate_evidence_from_candidate(
        execution_candidate.build_research_applicability_campaign_execution_candidate_v1()
    )


def _profile_by_name(review_package: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        profile.get("dataset_profile"): profile
        for profile in review_package.get("planned_inputs") or []
        if isinstance(profile, dict)
    }


def _planned_outputs_not_generated(outputs: Any) -> bool:
    return isinstance(outputs, list) and bool(outputs) and all(
        isinstance(output, dict)
        and output.get("status") == execution_candidate.PLANNED_NOT_GENERATED
        and output.get("generated") is False
        for output in outputs
    )


def _planned_outputs_research_only(outputs: Any) -> bool:
    return isinstance(outputs, list) and bool(outputs) and all(
        isinstance(output, dict)
        and output.get("output_label") == execution_candidate.RESEARCH_ONLY_NON_ACTIONABLE
        for output in outputs
    )


def _build_checklist(review_package: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        _check(
            "execution_candidate_kind_matches",
            execution_candidate.ARTIFACT_KIND_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_CANDIDATE,
            review_package.get("reviewed_execution_candidate_kind"),
        ),
        _check(
            "execution_candidate_status_ready_for_review",
            execution_candidate.RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_READY_FOR_OPERATOR_REVIEW,
            review_package.get("reviewed_execution_candidate_status"),
        ),
        _check(
            "execution_candidate_digest_matches",
            EXPECTED_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_CANDIDATE_DIGEST,
            review_package.get("reviewed_execution_candidate_digest"),
        ),
        _check(
            "execution_request_id_matches",
            execution_candidate.CAMPAIGN_EXECUTION_REQUEST_ID,
            review_package.get("reviewed_execution_request_id"),
        ),
        _check(
            "execution_candidate_checklist_zero_blockers",
            0,
            review_package.get("reviewed_candidate_blocker_count"),
        ),
        _check(
            "campaign_plan_digest_bound",
            execution_candidate.EXPECTED_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_DIGEST,
            review_package.get("research_campaign_plan_digest"),
        ),
        _check(
            "campaign_plan_review_digest_bound",
            execution_candidate.EXPECTED_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_REVIEW_PACKAGE_DIGEST,
            review_package.get("research_campaign_plan_review_package_digest"),
        ),
        _check(
            "dataset_availability_review_digest_bound",
            execution_candidate.EXPECTED_DATASET_FILE_AVAILABILITY_VERIFICATION_REVIEW_PACKAGE_DIGEST,
            review_package.get("dataset_file_availability_verification_review_package_digest"),
        ),
        _check(
            "read_only_discovery_review_digest_bound",
            execution_candidate.EXPECTED_READ_ONLY_DISCOVERY_REVIEW_PACKAGE_DIGEST,
            review_package.get("read_only_discovery_review_package_digest"),
        ),
        _check(
            "runtime_migration_review_digest_bound",
            execution_candidate.EXPECTED_RUNTIME_MIGRATION_REVIEW_PACKAGE_DIGEST,
            review_package.get("runtime_migration_review_package_digest"),
        ),
        _check(
            "swing_registry_approval_digest_bound",
            execution_candidate.plan_review.campaign_plan.availability_review.verification.discovery.runtime_planning.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST,
            review_package.get("swing_registry_approval_digest"),
        ),
        _check(
            "position_swing_registry_approval_digest_bound",
            execution_candidate.plan_review.campaign_plan.availability_review.verification.discovery.runtime_planning.EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST,
            review_package.get("position_swing_registry_approval_digest"),
        ),
        _check("campaign_scope_research_only", "RESEARCH_ONLY", review_package.get("campaign_scope")),
        _check("ticker_universe_aapl_only", ["AAPL"], review_package.get("ticker_universe")),
        _check(
            "profiles_swing_and_position_swing",
            ["POSITION_SWING", "SWING"],
            sorted(review_package.get("dataset_profiles") or []),
        ),
        _check(
            "date_range_matches",
            {"start": execution_candidate.DATE_RANGE_START, "end": execution_candidate.DATE_RANGE_END},
            {
                "start": review_package.get("date_range_start"),
                "end": review_package.get("date_range_end"),
            },
        ),
        _check(
            "execution_mode_read_only_offline_research",
            execution_candidate.READ_ONLY_OFFLINE_RESEARCH,
            review_package.get("execution_mode"),
        ),
        _check("runtime_mode_not_runtime", execution_candidate.NOT_RUNTIME, review_package.get("runtime_mode")),
        _check(
            "strategy_mode_not_strategy_input",
            execution_candidate.NOT_STRATEGY_INPUT,
            review_package.get("strategy_mode"),
        ),
        _check("broker_mode_disabled", execution_candidate.DISABLED, review_package.get("broker_mode")),
        _check(
            "paper_trading_mode_disabled",
            execution_candidate.DISABLED,
            review_package.get("paper_trading_mode"),
        ),
        _check("planned_outputs_not_generated", True, _planned_outputs_not_generated(review_package.get("planned_outputs"))),
        _check(
            "planned_outputs_research_only_non_actionable",
            True,
            _planned_outputs_research_only(review_package.get("planned_outputs")),
        ),
        _check("execution_gates_defined", execution_candidate.EXECUTION_GATES, review_package.get("execution_gates")),
        _check("risk_controls_defined", execution_candidate.RISK_CONTROLS, review_package.get("risk_controls")),
        _check("campaign_execution_authorized_false", False, review_package.get("campaign_execution_authorized")),
        _check("campaign_execution_performed_false", False, review_package.get("campaign_execution_performed")),
        _check("campaign_results_generated_false", False, review_package.get("campaign_results_generated")),
        _check(
            "provider_requests_made_in_review_false",
            False,
            review_package.get("provider_requests_made_in_review"),
        ),
        _check("runtime_migration_approved_false", False, review_package.get("runtime_migration_approved")),
        _check("runtime_migration_active_false", False, review_package.get("runtime_migration_active")),
        _check("strategy_runtime_migration_false", False, review_package.get("strategy_runtime_migration")),
        _check("runtime_use_not_authorized", execution_candidate.NOT_AUTHORIZED, review_package.get("runtime_use")),
        _check("strategy_use_not_authorized", execution_candidate.NOT_AUTHORIZED, review_package.get("strategy_use")),
        _check("paper_trading_not_authorized", execution_candidate.NOT_AUTHORIZED, review_package.get("paper_trading")),
        _check("broker_execution_not_authorized", execution_candidate.NOT_AUTHORIZED, review_package.get("broker_execution")),
        _check("automatic_stitching_false", False, review_package.get("automatic_stitching")),
        _check(
            "predictive_usefulness_not_accepted",
            acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
            review_package.get("predictive_usefulness"),
            severity=INFO,
        ),
        _check(
            "profitability_not_accepted",
            acquisition.PROFITABILITY_NOT_ACCEPTED,
            review_package.get("profitability"),
            severity=INFO,
        ),
        _check(
            "no_campaign_execution_artifact_created",
            False,
            review_package.get("campaign_execution_artifact_created"),
        ),
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
        "ready_for_operator_assessment": failed == 0,
        "operator_decision_required_before_campaign_execution": True,
        "software_campaign_execution_authorized": False,
        "software_runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def _digest_payload(review_package: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(review_package)
    payload.pop("research_applicability_campaign_execution_candidate_review_package_digest", None)
    return payload


def research_applicability_campaign_execution_candidate_review_package_digest_v1(
    review_package: dict[str, Any],
) -> str:
    """Return the deterministic semantic digest for an execution candidate review package."""
    return semantic_digest(_digest_payload(review_package))


def build_research_applicability_campaign_execution_candidate_review_package_v1(
    execution_candidate: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build an offline operator review package without authorizing campaign execution."""
    binding_mode = RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_CANDIDATE_STATUS_BINDING
    evidence = _recorded_candidate_evidence()
    if execution_candidate is not None:
        binding_mode = RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_CANDIDATE_OBJECT_BINDING
        evidence = _candidate_evidence_from_candidate(execution_candidate)
    review_package = {
        **_review_context(),
        "binding_mode": binding_mode,
        **evidence,
        "remaining_required_tasks": list(REMAINING_REQUIRED_TASKS),
    }
    checklist = _build_checklist(review_package)
    review_package["review_checklist"] = checklist
    review_package["review_summary"] = _summary(checklist)
    review_package["research_applicability_campaign_execution_candidate_review_package_digest"] = (
        research_applicability_campaign_execution_candidate_review_package_digest_v1(review_package)
    )
    validate_research_applicability_campaign_execution_candidate_review_package_v1(review_package)
    return review_package


def _reject_forbidden_values(mapping: dict[str, Any], *, path: str = "review_package") -> None:
    for key, value in mapping.items():
        current_path = f"{path}.{key}"
        if isinstance(value, str) and value in {
            "RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTED",
            "RESEARCH_APPLICABILITY_CAMPAIGN_RESULTS",
            "RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_APPROVED",
            "PREDICTIVE_USEFULNESS_ACCEPTED",
            "PROFITABILITY_ACCEPTED",
            "RUNTIME_MIGRATION_APPROVED",
            "RUNTIME_MIGRATION_ACTIVE",
            "STRATEGY_RUNTIME_MIGRATION",
            "STRATEGY_RUNTIME_MIGRATION_ACTIVE",
        }:
            raise ResearchApplicabilityCampaignExecutionCandidateOperatorReviewError(
                f"{current_path} must not emit {value}"
            )
        if key in FORBIDDEN_APPROVAL_FIELDS and value is not None:
            raise ResearchApplicabilityCampaignExecutionCandidateOperatorReviewError(
                f"{current_path} must be null"
            )
        if key in {
            "campaign_execution_authorized",
            "campaign_execution_performed",
            "campaign_results_generated",
            "campaign_execution_artifact_created",
            "runtime_migration_approved",
            "runtime_migration_active",
            "strategy_runtime_migration",
            "automatic_stitching",
            "provider_requests_made_in_review",
            "software_campaign_execution_authorized",
            "software_runtime_migration_authorized",
            "software_runtime_activation_authorized",
            "generated",
            "execution_performed",
            "output_generated",
        } and value is True:
            raise ResearchApplicabilityCampaignExecutionCandidateOperatorReviewError(
                f"{current_path} must be false"
            )
        if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and value == "AUTHORIZED":
            raise ResearchApplicabilityCampaignExecutionCandidateOperatorReviewError(
                f"{current_path} must not be AUTHORIZED"
            )
        if key in {"predictive_usefulness", "profitability"} and value == "accepted":
            raise ResearchApplicabilityCampaignExecutionCandidateOperatorReviewError(
                f"{current_path} must not be accepted"
            )
        if isinstance(value, dict):
            _reject_forbidden_values(value, path=current_path)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, dict):
                    _reject_forbidden_values(item, path=f"{current_path}[{index}]")


def _validate_planned_inputs(review_package: dict[str, Any]) -> None:
    inputs = review_package.get("planned_inputs")
    if not isinstance(inputs, list) or len(inputs) != 2:
        raise ResearchApplicabilityCampaignExecutionCandidateOperatorReviewError(
            "planned_inputs must contain SWING and POSITION_SWING"
        )
    by_profile = _profile_by_name(review_package)
    if "SWING" not in by_profile:
        raise ResearchApplicabilityCampaignExecutionCandidateOperatorReviewError(
            "missing SWING planned input"
        )
    if "POSITION_SWING" not in by_profile:
        raise ResearchApplicabilityCampaignExecutionCandidateOperatorReviewError(
            "missing POSITION_SWING planned input"
        )
    expected = {
        profile["dataset_profile"]: profile
        for profile in execution_candidate.build_research_applicability_campaign_execution_candidate_v1()[
            "planned_inputs"
        ]
    }
    for profile, expected_profile in expected.items():
        candidate_profile = by_profile[profile]
        for field, expected_value in expected_profile.items():
            _expect(candidate_profile.get(field), expected_value, field)


def _validate_planning_lists(review_package: dict[str, Any]) -> None:
    _expect(
        review_package.get("planned_outputs"),
        execution_candidate._planned_outputs(),
        "planned_outputs",
    )
    _expect(
        review_package.get("execution_gates"),
        execution_candidate.EXECUTION_GATES,
        "execution_gates",
    )
    _expect(review_package.get("risk_controls"), execution_candidate.RISK_CONTROLS, "risk_controls")
    _expect(
        review_package.get("remaining_required_tasks"),
        REMAINING_REQUIRED_TASKS,
        "remaining_required_tasks",
    )


def validate_research_applicability_campaign_execution_candidate_review_package_v1(
    review_package: dict[str, Any],
) -> dict[str, Any]:
    """Validate an execution candidate review package without authorizing execution."""
    if not isinstance(review_package, dict):
        raise ResearchApplicabilityCampaignExecutionCandidateOperatorReviewError(
            "research applicability campaign execution candidate review package must be a JSON object"
        )
    _reject_forbidden_values(review_package)
    _expect(
        review_package.get("artifact_kind"),
        ARTIFACT_KIND_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_CANDIDATE_REVIEW_PACKAGE,
        "artifact_kind",
    )
    _expect(
        review_package.get("schema_version"),
        SCHEMA_VERSION_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_CANDIDATE_REVIEW_V1,
        "schema_version",
    )
    _expect(
        review_package.get("review_status"),
        RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_CANDIDATE_REVIEW_PACKAGE_READY,
        "review_status",
    )
    if review_package.get("binding_mode") not in {
        RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_CANDIDATE_STATUS_BINDING,
        RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_CANDIDATE_OBJECT_BINDING,
    }:
        raise ResearchApplicabilityCampaignExecutionCandidateOperatorReviewError(
            "binding_mode mismatch"
        )
    _expect_true(review_package.get("operator_decision_required"), "operator_decision_required")
    _expect(review_package.get("operator_decision"), None, "operator_decision")
    for field in FORBIDDEN_APPROVAL_FIELDS:
        _expect(review_package.get(field), None, field)
    _expect_true(review_package.get("created_offline"), "created_offline")
    for field in (
        "campaign_execution_authorized",
        "campaign_execution_performed",
        "campaign_results_generated",
        "campaign_execution_artifact_created",
        "provider_requests_made_in_review",
        "runtime_migration_approved",
        "runtime_migration_active",
        "strategy_runtime_migration",
        "automatic_stitching",
        "software_campaign_execution_authorized",
        "software_runtime_migration_authorized",
        "software_runtime_activation_authorized",
    ):
        _expect_false(review_package.get(field), field)
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(review_package.get(field), execution_candidate.NOT_AUTHORIZED, field)
    _expect(
        review_package.get("predictive_usefulness"),
        acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "predictive_usefulness",
    )
    _expect(review_package.get("profitability"), acquisition.PROFITABILITY_NOT_ACCEPTED, "profitability")
    for field, expected in {
        "reviewed_execution_candidate_kind": (
            execution_candidate.ARTIFACT_KIND_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_CANDIDATE
        ),
        "reviewed_execution_candidate_status": (
            execution_candidate.RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_READY_FOR_OPERATOR_REVIEW
        ),
        "reviewed_execution_candidate_digest": (
            EXPECTED_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_CANDIDATE_DIGEST
        ),
        "reviewed_execution_request_id": execution_candidate.CAMPAIGN_EXECUTION_REQUEST_ID,
        "reviewed_candidate_checklist_total": EXPECTED_CANDIDATE_CHECKLIST_TOTAL,
        "reviewed_candidate_checklist_passed": EXPECTED_CANDIDATE_CHECKLIST_PASSED,
        "reviewed_candidate_checklist_failed": EXPECTED_CANDIDATE_CHECKLIST_FAILED,
        "reviewed_candidate_blocker_count": EXPECTED_CANDIDATE_BLOCKER_COUNT,
        "campaign_scope": "RESEARCH_ONLY",
        "ticker_universe": ["AAPL"],
        "dataset_profiles": ["SWING", "POSITION_SWING"],
        "date_range_start": execution_candidate.DATE_RANGE_START,
        "date_range_end": execution_candidate.DATE_RANGE_END,
        "execution_mode": execution_candidate.READ_ONLY_OFFLINE_RESEARCH,
        "runtime_mode": execution_candidate.NOT_RUNTIME,
        "strategy_mode": execution_candidate.NOT_STRATEGY_INPUT,
        "broker_mode": execution_candidate.DISABLED,
        "paper_trading_mode": execution_candidate.DISABLED,
        "planned_output_count": len(execution_candidate.PLANNED_OUTPUT_NAMES),
        "planned_outputs_status": execution_candidate.PLANNED_NOT_GENERATED,
        "planned_outputs_label": execution_candidate.RESEARCH_ONLY_NON_ACTIONABLE,
        "research_campaign_plan_digest": (
            execution_candidate.EXPECTED_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_DIGEST
        ),
        "research_campaign_plan_review_package_digest": (
            execution_candidate.EXPECTED_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_REVIEW_PACKAGE_DIGEST
        ),
        "dataset_file_availability_verification_review_package_digest": (
            execution_candidate.EXPECTED_DATASET_FILE_AVAILABILITY_VERIFICATION_REVIEW_PACKAGE_DIGEST
        ),
        "read_only_discovery_review_package_digest": (
            execution_candidate.EXPECTED_READ_ONLY_DISCOVERY_REVIEW_PACKAGE_DIGEST
        ),
        "runtime_migration_review_package_digest": (
            execution_candidate.EXPECTED_RUNTIME_MIGRATION_REVIEW_PACKAGE_DIGEST
        ),
        "swing_registry_approval_digest": (
            execution_candidate.plan_review.campaign_plan.availability_review.verification.discovery.runtime_planning.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST
        ),
        "position_swing_registry_approval_digest": (
            execution_candidate.plan_review.campaign_plan.availability_review.verification.discovery.runtime_planning.EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST
        ),
    }.items():
        _expect(review_package.get(field), expected, field)
    _validate_planned_inputs(review_package)
    _validate_planning_lists(review_package)
    checklist = review_package.get("review_checklist")
    if not isinstance(checklist, list):
        raise ResearchApplicabilityCampaignExecutionCandidateOperatorReviewError(
            "review_checklist must be a list"
        )
    _expect(
        [item.get("check_id") for item in checklist if isinstance(item, dict)],
        REQUIRED_CHECK_IDS,
        "review_checklist check IDs",
    )
    expected_checklist = _build_checklist(review_package)
    failed = [item for item in expected_checklist if item["status"] != PASS]
    if failed:
        raise ResearchApplicabilityCampaignExecutionCandidateOperatorReviewError(
            "research applicability campaign execution candidate review checklist contains "
            f"failed check: {failed[0]['check_id']}"
        )
    _expect(checklist, expected_checklist, "review_checklist")
    summary = _summary(checklist)
    _expect(review_package.get("review_summary"), summary, "review_summary")
    _expect_true(summary.get("ready_for_operator_assessment"), "ready_for_operator_assessment")
    _expect_true(
        summary.get("operator_decision_required_before_campaign_execution"),
        "operator_decision_required_before_campaign_execution",
    )
    _expect_false(summary.get("software_campaign_execution_authorized"), "software_campaign_execution_authorized")
    _expect_false(summary.get("software_runtime_migration_authorized"), "software_runtime_migration_authorized")
    _expect_false(summary.get("software_runtime_activation_authorized"), "software_runtime_activation_authorized")
    digest = review_package.get("research_applicability_campaign_execution_candidate_review_package_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise ResearchApplicabilityCampaignExecutionCandidateOperatorReviewError(
            "research_applicability_campaign_execution_candidate_review_package_digest missing"
        )
    _expect(
        digest,
        research_applicability_campaign_execution_candidate_review_package_digest_v1(review_package),
        "research_applicability_campaign_execution_candidate_review_package_digest",
    )
    return {
        "status": "RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_CANDIDATE_REVIEW_PACKAGE_VALID",
        "artifact_kind": review_package["artifact_kind"],
        "review_status": review_package["review_status"],
        "research_applicability_campaign_execution_candidate_review_package_digest": digest,
        "reviewed_execution_candidate_digest": (
            EXPECTED_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_CANDIDATE_DIGEST
        ),
        "reviewed_execution_request_id": execution_candidate.CAMPAIGN_EXECUTION_REQUEST_ID,
        "research_campaign_plan_digest": (
            execution_candidate.EXPECTED_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_DIGEST
        ),
        "research_campaign_plan_review_package_digest": (
            execution_candidate.EXPECTED_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_REVIEW_PACKAGE_DIGEST
        ),
        "dataset_file_availability_verification_review_package_digest": (
            execution_candidate.EXPECTED_DATASET_FILE_AVAILABILITY_VERIFICATION_REVIEW_PACKAGE_DIGEST
        ),
        "swing_registry_approval_digest": review_package["swing_registry_approval_digest"],
        "position_swing_registry_approval_digest": review_package[
            "position_swing_registry_approval_digest"
        ],
        "campaign_scope": "RESEARCH_ONLY",
        "ticker_universe": ["AAPL"],
        "dataset_profiles": ["SWING", "POSITION_SWING"],
        "total_checks": summary["total_checks"],
        "passed_checks": summary["passed_checks"],
        "failed_checks": summary["failed_checks"],
        "blocker_count": summary["blocker_count"],
        "campaign_execution_authorized": False,
        "campaign_execution_performed": False,
        "campaign_results_generated": False,
        "runtime_migration_approved": False,
        "runtime_migration_active": False,
        "strategy_runtime_migration": False,
        "runtime_use": execution_candidate.NOT_AUTHORIZED,
        "strategy_use": execution_candidate.NOT_AUTHORIZED,
        "paper_trading": execution_candidate.NOT_AUTHORIZED,
        "broker_execution": execution_candidate.NOT_AUTHORIZED,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
    }


def build_research_applicability_campaign_execution_candidate_review_markdown_v1(
    review_package: dict[str, Any],
) -> str:
    """Render a sanitized research applicability execution candidate review status document."""
    validation = validate_research_applicability_campaign_execution_candidate_review_package_v1(
        review_package
    )
    summary = review_package["review_summary"]
    lines = [
        "# MarketFlow Research Applicability Campaign Execution Candidate Operator Review Package Status",
        "",
        "## Title",
        "- Research Applicability Campaign Execution Candidate Operator Review Package v1.",
        "",
        "## Reviewed Execution Candidate",
        f"- Review package artifact kind: `{review_package['artifact_kind']}`",
        f"- Review status: `{review_package['review_status']}`",
        f"- Binding mode: `{review_package['binding_mode']}`",
        f"- Reviewed execution candidate kind: `{review_package['reviewed_execution_candidate_kind']}`",
        f"- Reviewed execution candidate status: `{review_package['reviewed_execution_candidate_status']}`",
        f"- Reviewed execution candidate digest: `{review_package['reviewed_execution_candidate_digest']}`",
        f"- Reviewed execution request ID: `{review_package['reviewed_execution_request_id']}`",
        "",
        "## Execution Request Scope",
        f"- Campaign scope: `{review_package['campaign_scope']}`",
        f"- Ticker universe: `{', '.join(review_package['ticker_universe'])}`",
        f"- Dataset profiles: `{', '.join(review_package['dataset_profiles'])}`",
        f"- Date range: `{review_package['date_range_start']}` through `{review_package['date_range_end']}`",
        f"- Execution mode: `{review_package['execution_mode']}`",
        f"- Runtime mode: `{review_package['runtime_mode']}`",
        f"- Strategy mode: `{review_package['strategy_mode']}`",
        "",
        "## Source Evidence",
        f"- Campaign plan digest: `{review_package['research_campaign_plan_digest']}`",
        f"- Campaign plan review package digest: `{review_package['research_campaign_plan_review_package_digest']}`",
        f"- Dataset availability review digest: `{review_package['dataset_file_availability_verification_review_package_digest']}`",
        f"- Read-only discovery review digest: `{review_package['read_only_discovery_review_package_digest']}`",
        f"- Runtime migration review digest: `{review_package['runtime_migration_review_package_digest']}`",
        f"- SWING registry approval digest: `{review_package['swing_registry_approval_digest']}`",
        f"- POSITION_SWING registry approval digest: `{review_package['position_swing_registry_approval_digest']}`",
        "",
        "## Planned Inputs",
    ]
    for profile in review_package["planned_inputs"]:
        lines.extend(
            [
                f"- `{profile['registry_key']}`",
                f"  - Planned dataset path: `{profile['planned_dataset_path']}`",
                f"  - Runtime use: `{profile['runtime_use']}`",
                f"  - Strategy use: `{profile['strategy_use']}`",
            ]
        )
    lines.extend(["", "## Planned Outputs"])
    lines.extend(
        f"- `{output['name']}`: `{output['status']}` / generated `{output['generated']}` / label `{output['output_label']}`"
        for output in review_package["planned_outputs"]
    )
    lines.extend(["", "## Execution Gates"])
    lines.extend(f"- `{gate}`" for gate in review_package["execution_gates"])
    lines.extend(["", "## Risk Controls"])
    lines.extend(f"- {control}" for control in review_package["risk_controls"])
    lines.extend(
        [
            "",
            "## Runtime Boundary",
            f"- campaign_execution_authorized: `{review_package['campaign_execution_authorized']}`",
            f"- campaign_execution_performed: `{review_package['campaign_execution_performed']}`",
            f"- campaign_results_generated: `{review_package['campaign_results_generated']}`",
            f"- provider_requests_made_in_review: `{review_package['provider_requests_made_in_review']}`",
            f"- runtime_migration_approved: `{review_package['runtime_migration_approved']}`",
            f"- runtime_migration_active: `{review_package['runtime_migration_active']}`",
            f"- strategy_runtime_migration: `{review_package['strategy_runtime_migration']}`",
            f"- runtime_use: `{review_package['runtime_use']}`",
            f"- strategy_use: `{review_package['strategy_use']}`",
            f"- paper_trading: `{review_package['paper_trading']}`",
            f"- broker_execution: `{review_package['broker_execution']}`",
            f"- automatic_stitching: `{review_package['automatic_stitching']}`",
            f"- predictive_usefulness: `{review_package['predictive_usefulness']}`",
            f"- profitability: `{review_package['profitability']}`",
            "",
            "## Checklist Summary",
            f"- Total checks: `{summary['total_checks']}`",
            f"- Passed checks: `{summary['passed_checks']}`",
            f"- Failed checks: `{summary['failed_checks']}`",
            f"- Blocker count: `{summary['blocker_count']}`",
            "",
            "## Remaining Required Tasks",
        ]
    )
    lines.extend(f"{index}. {task}" for index, task in enumerate(review_package["remaining_required_tasks"], start=1))
    lines.extend(
        [
            "",
            "## Guardrails",
            "- Created offline: `True`",
            "- Provider requests made in review: `False`",
            "- Campaign execution authorized: `False`",
            "- Campaign execution performed: `False`",
            "- Campaign results generated: `False`",
            "- No Massive.com / Polygon provider data was fetched.",
            "- No walk-forward validation or strategy scoring was run.",
            "- No runtime default source was changed.",
            "- Runtime, Strategy, paper trading, and broker execution use remain `NOT_AUTHORIZED`.",
            "- Predictive usefulness and profitability remain not accepted.",
            "",
            "## Review Package Digest",
            f"- Review package digest: `{validation['research_applicability_campaign_execution_candidate_review_package_digest']}`",
            "",
        ]
    )
    return "\n".join(lines)


def write_research_applicability_campaign_execution_candidate_review_package_v1(
    output_dir: str | Path,
    *,
    execution_candidate: dict[str, Any] | None = None,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write the execution candidate review package JSON artifact without overwriting output."""
    review_package = build_research_applicability_campaign_execution_candidate_review_package_v1(
        execution_candidate
    )
    validation = validate_research_applicability_campaign_execution_candidate_review_package_v1(
        review_package
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "research_applicability_campaign_execution_candidate_review_package_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise ResearchApplicabilityCampaignExecutionCandidateOperatorReviewError(
            "research applicability campaign execution candidate review filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise ResearchApplicabilityCampaignExecutionCandidateOperatorReviewError(
            "research applicability campaign execution candidate review output already exists"
        )
    payload = canonical_json_bytes(review_package)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": str(path),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
    }
