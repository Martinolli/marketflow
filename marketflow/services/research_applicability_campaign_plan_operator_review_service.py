"""Offline operator-review package for research applicability campaign plans."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import research_applicability_campaign_plan_service as campaign_plan


ARTIFACT_KIND_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_CANDIDATE_REVIEW_PACKAGE = (
    "RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_CANDIDATE_REVIEW_PACKAGE"
)
SCHEMA_VERSION_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_CANDIDATE_REVIEW_V1 = (
    "research_applicability_campaign_plan_candidate_review_v1"
)
RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_CANDIDATE_REVIEW_PACKAGE_READY = (
    "RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_CANDIDATE_REVIEW_PACKAGE_READY"
)
RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_STATUS_BINDING = (
    "RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_STATUS_BINDING"
)
RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_OBJECT_BINDING = (
    "RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_OBJECT_BINDING"
)
CAMPAIGN_TOUCHPOINT_INVENTORY_INCOMPLETE_COMPACT = "INCOMPLETE_COMPACT"

EXPECTED_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_DIGEST = (
    "b376bce431248be913dfe5c534535104a1663a5491a16560c9989681c323b97e"
)
EXPECTED_PLAN_CHECKLIST_TOTAL = len(campaign_plan.REQUIRED_CHECK_IDS)
EXPECTED_PLAN_CHECKLIST_PASSED = len(campaign_plan.REQUIRED_CHECK_IDS)
EXPECTED_PLAN_CHECKLIST_FAILED = 0
EXPECTED_PLAN_BLOCKER_COUNT = 0

PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
INFO = "INFO"

REQUIRED_CHECK_IDS = [
    "campaign_plan_kind_matches",
    "campaign_plan_status_ready_for_review",
    "campaign_plan_digest_matches",
    "campaign_plan_checklist_zero_blockers",
    "dataset_availability_review_digest_bound",
    "read_only_discovery_review_digest_bound",
    "runtime_migration_review_digest_bound",
    "swing_registry_approval_digest_bound",
    "position_swing_registry_approval_digest_bound",
    "campaign_scope_research_only",
    "campaign_ticker_universe_aapl_only",
    "campaign_profiles_swing_and_position_swing",
    "campaign_range_matches",
    "planned_questions_confirmed",
    "planned_metrics_descriptive_only",
    "planned_outputs_research_only",
    "future_execution_gates_defined",
    "risk_controls_defined",
    "touchpoint_inventory_present",
    "touchpoint_inventory_incomplete_compact_acknowledged",
    "campaign_execution_authorized_false",
    "campaign_execution_performed_false",
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
    "Research-only applicability campaign execution candidate.",
    "Research-only applicability campaign execution operator review.",
    "Research-only applicability campaign execution, if approved.",
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


class ResearchApplicabilityCampaignPlanOperatorReviewError(ValueError):
    """Raised when a research applicability plan review package violates guardrails."""


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
        raise ResearchApplicabilityCampaignPlanOperatorReviewError(f"{field_name} mismatch")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise ResearchApplicabilityCampaignPlanOperatorReviewError(f"{field_name} must be false")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise ResearchApplicabilityCampaignPlanOperatorReviewError(f"{field_name} must be true")


def _review_context() -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_CANDIDATE_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_CANDIDATE_REVIEW_V1,
        "review_status": RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_CANDIDATE_REVIEW_PACKAGE_READY,
        "operator_decision_required": True,
        "operator_decision": None,
        "operator_approved_by": None,
        "operator_approval_timestamp": None,
        "operator_approval_digest": None,
        "operator_signature": None,
        "approval_status": None,
        "campaign_execution_authorized": False,
        "campaign_execution_performed": False,
        "runtime_migration_approved": False,
        "runtime_migration_active": False,
        "strategy_runtime_migration": False,
        "runtime_use": campaign_plan.NOT_AUTHORIZED,
        "strategy_use": campaign_plan.NOT_AUTHORIZED,
        "paper_trading": campaign_plan.NOT_AUTHORIZED,
        "broker_execution": campaign_plan.NOT_AUTHORIZED,
        "automatic_stitching": False,
        "created_offline": True,
        "provider_requests_made_in_review": False,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "software_campaign_execution_authorized": False,
        "software_runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def _profile_by_name(review_package: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        profile.get("dataset_profile"): profile
        for profile in review_package.get("campaign_profiles") or []
        if isinstance(profile, dict)
    }


def _scope_from_plan(plan: dict[str, Any]) -> str:
    scope = plan.get("campaign_scope") or {}
    if scope.get("scope_type") == "RESEARCH_ONLY_APPLICABILITY" and plan.get("research_only") is True:
        return "RESEARCH_ONLY"
    return str(scope.get("scope_type"))


def _plan_evidence_from_candidate(plan: dict[str, Any]) -> dict[str, Any]:
    try:
        validation = campaign_plan.validate_research_applicability_campaign_plan_candidate_v1(plan)
    except campaign_plan.ResearchApplicabilityCampaignPlanError as exc:
        raise ResearchApplicabilityCampaignPlanOperatorReviewError(
            f"source research applicability campaign plan invalid: {exc}"
        ) from exc
    return {
        "reviewed_plan_kind": plan["artifact_kind"],
        "reviewed_plan_status": plan["plan_status"],
        "reviewed_plan_digest": validation["research_applicability_campaign_plan_digest"],
        "reviewed_plan_checklist_total": validation["total_checks"],
        "reviewed_plan_checklist_passed": validation["passed_checks"],
        "reviewed_plan_checklist_failed": validation["failed_checks"],
        "reviewed_plan_blocker_count": validation["blocker_count"],
        "campaign_scope": _scope_from_plan(plan),
        "campaign_ticker_universe": list(plan["campaign_ticker_universe"]),
        "campaign_profiles": deepcopy(plan["campaign_profiles"]),
        "campaign_range_start": plan["campaign_date_range"]["start"],
        "campaign_range_end": plan["campaign_date_range"]["end"],
        "campaign_touchpoint_inventory_count": len(plan["campaign_touchpoint_inventory"]),
        "campaign_touchpoint_inventory_status": CAMPAIGN_TOUCHPOINT_INVENTORY_INCOMPLETE_COMPACT,
        "campaign_touchpoint_inventory": deepcopy(plan["campaign_touchpoint_inventory"]),
        "dataset_file_availability_verification_review_package_digest": plan[
            "dataset_file_availability_verification_review_package_digest"
        ],
        "dataset_file_availability_verification_package_digest": plan[
            "dataset_file_availability_verification_package_digest"
        ],
        "read_only_discovery_review_package_digest": plan["read_only_discovery_review_package_digest"],
        "runtime_migration_review_package_digest": plan["runtime_migration_review_package_digest"],
        "swing_registry_approval_digest": validation["swing_registry_approval_digest"],
        "position_swing_registry_approval_digest": validation["position_swing_registry_approval_digest"],
        "campaign_questions": list(plan["campaign_questions"]),
        "planned_metrics": deepcopy(plan["planned_metrics"]),
        "planned_outputs": deepcopy(plan["planned_outputs"]),
        "future_execution_gates": list(plan["operator_gates"]),
        "risk_controls": list(plan["risk_controls"]),
    }


def _recorded_plan_evidence() -> dict[str, Any]:
    return _plan_evidence_from_candidate(campaign_plan.build_research_applicability_campaign_plan_candidate_v1())


def _planned_metrics_descriptive_only(metrics: list[dict[str, Any]] | None) -> bool:
    if not metrics:
        return False
    allowed = {"RESEARCH_DESCRIPTIVE_ONLY", campaign_plan.RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE}
    return all(metric.get("classification") in allowed for metric in metrics if isinstance(metric, dict))


def _planned_outputs_research_only(outputs: list[dict[str, Any]] | None) -> bool:
    if not outputs:
        return False
    return all(
        output.get("status") == campaign_plan.RESEARCH_ONLY_PLANNED_NOT_CREATED
        for output in outputs
        if isinstance(output, dict)
    )


def _build_checklist(review_package: dict[str, Any]) -> list[dict[str, Any]]:
    profiles = _profile_by_name(review_package)
    return [
        _check(
            "campaign_plan_kind_matches",
            campaign_plan.ARTIFACT_KIND_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_CANDIDATE,
            review_package.get("reviewed_plan_kind"),
        ),
        _check(
            "campaign_plan_status_ready_for_review",
            campaign_plan.RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_READY_FOR_OPERATOR_REVIEW,
            review_package.get("reviewed_plan_status"),
        ),
        _check(
            "campaign_plan_digest_matches",
            EXPECTED_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_DIGEST,
            review_package.get("reviewed_plan_digest"),
        ),
        _check(
            "campaign_plan_checklist_zero_blockers",
            {
                "total": EXPECTED_PLAN_CHECKLIST_TOTAL,
                "passed": EXPECTED_PLAN_CHECKLIST_PASSED,
                "failed": EXPECTED_PLAN_CHECKLIST_FAILED,
                "blockers": EXPECTED_PLAN_BLOCKER_COUNT,
            },
            {
                "total": review_package.get("reviewed_plan_checklist_total"),
                "passed": review_package.get("reviewed_plan_checklist_passed"),
                "failed": review_package.get("reviewed_plan_checklist_failed"),
                "blockers": review_package.get("reviewed_plan_blocker_count"),
            },
        ),
        _check(
            "dataset_availability_review_digest_bound",
            campaign_plan.EXPECTED_DATASET_FILE_AVAILABILITY_VERIFICATION_REVIEW_PACKAGE_DIGEST,
            review_package.get("dataset_file_availability_verification_review_package_digest"),
        ),
        _check(
            "read_only_discovery_review_digest_bound",
            campaign_plan.EXPECTED_READ_ONLY_DISCOVERY_REVIEW_PACKAGE_DIGEST,
            review_package.get("read_only_discovery_review_package_digest"),
        ),
        _check(
            "runtime_migration_review_digest_bound",
            campaign_plan.EXPECTED_RUNTIME_MIGRATION_REVIEW_PACKAGE_DIGEST,
            review_package.get("runtime_migration_review_package_digest"),
        ),
        _check(
            "swing_registry_approval_digest_bound",
            campaign_plan.availability_review.verification.discovery.runtime_planning.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST,
            review_package.get("swing_registry_approval_digest"),
        ),
        _check(
            "position_swing_registry_approval_digest_bound",
            campaign_plan.availability_review.verification.discovery.runtime_planning.EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST,
            review_package.get("position_swing_registry_approval_digest"),
        ),
        _check("campaign_scope_research_only", "RESEARCH_ONLY", review_package.get("campaign_scope")),
        _check("campaign_ticker_universe_aapl_only", ["AAPL"], review_package.get("campaign_ticker_universe")),
        _check("campaign_profiles_swing_and_position_swing", ["POSITION_SWING", "SWING"], sorted(profiles)),
        _check(
            "campaign_range_matches",
            {"start": "2022-01-01", "end": "2025-12-31"},
            {
                "start": review_package.get("campaign_range_start"),
                "end": review_package.get("campaign_range_end"),
            },
        ),
        _check("planned_questions_confirmed", campaign_plan.CAMPAIGN_QUESTIONS, review_package.get("campaign_questions")),
        _check(
            "planned_metrics_descriptive_only",
            True,
            _planned_metrics_descriptive_only(review_package.get("planned_metrics")),
        ),
        _check(
            "planned_outputs_research_only",
            True,
            _planned_outputs_research_only(review_package.get("planned_outputs")),
        ),
        _check(
            "future_execution_gates_defined",
            campaign_plan.FUTURE_EXECUTION_GATES,
            review_package.get("future_execution_gates"),
        ),
        _check("risk_controls_defined", campaign_plan.RISK_CONTROLS, review_package.get("risk_controls")),
        _check("touchpoint_inventory_present", True, bool(review_package.get("campaign_touchpoint_inventory"))),
        _check(
            "touchpoint_inventory_incomplete_compact_acknowledged",
            {
                "count": 8,
                "status": CAMPAIGN_TOUCHPOINT_INVENTORY_INCOMPLETE_COMPACT,
            },
            {
                "count": review_package.get("campaign_touchpoint_inventory_count"),
                "status": review_package.get("campaign_touchpoint_inventory_status"),
            },
        ),
        _check("campaign_execution_authorized_false", False, review_package.get("campaign_execution_authorized")),
        _check("campaign_execution_performed_false", False, review_package.get("campaign_execution_performed")),
        _check("provider_requests_made_in_review_false", False, review_package.get("provider_requests_made_in_review")),
        _check("runtime_migration_approved_false", False, review_package.get("runtime_migration_approved")),
        _check("runtime_migration_active_false", False, review_package.get("runtime_migration_active")),
        _check("strategy_runtime_migration_false", False, review_package.get("strategy_runtime_migration")),
        _check("runtime_use_not_authorized", campaign_plan.NOT_AUTHORIZED, review_package.get("runtime_use")),
        _check("strategy_use_not_authorized", campaign_plan.NOT_AUTHORIZED, review_package.get("strategy_use")),
        _check("paper_trading_not_authorized", campaign_plan.NOT_AUTHORIZED, review_package.get("paper_trading")),
        _check("broker_execution_not_authorized", campaign_plan.NOT_AUTHORIZED, review_package.get("broker_execution")),
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
            {
                "artifact_kind_is_review_package": True,
                "review_status_is_review_ready": True,
                "approval_status_is_null": True,
                "campaign_execution_authorized_is_false": True,
                "campaign_execution_performed_is_false": True,
            },
            {
                "artifact_kind_is_review_package": review_package.get("artifact_kind")
                == ARTIFACT_KIND_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_CANDIDATE_REVIEW_PACKAGE,
                "review_status_is_review_ready": review_package.get("review_status")
                == RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_CANDIDATE_REVIEW_PACKAGE_READY,
                "approval_status_is_null": review_package.get("approval_status") is None,
                "campaign_execution_authorized_is_false": review_package.get("campaign_execution_authorized")
                is False,
                "campaign_execution_performed_is_false": review_package.get("campaign_execution_performed")
                is False,
            },
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
    payload.pop("research_applicability_campaign_plan_review_package_digest", None)
    return payload


def research_applicability_campaign_plan_review_package_digest_v1(
    review_package: dict[str, Any],
) -> str:
    """Return the deterministic semantic digest for a campaign plan review package."""
    return semantic_digest(_digest_payload(review_package))


def build_research_applicability_campaign_plan_candidate_review_package_v1(
    campaign_plan: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build an offline operator review package for a research campaign plan."""
    binding_mode = RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_STATUS_BINDING
    evidence = _recorded_plan_evidence()
    if campaign_plan is not None:
        binding_mode = RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_OBJECT_BINDING
        evidence = _plan_evidence_from_candidate(campaign_plan)
    review_package = {
        **_review_context(),
        "binding_mode": binding_mode,
        **evidence,
        "remaining_required_tasks": list(REMAINING_REQUIRED_TASKS),
    }
    checklist = _build_checklist(review_package)
    review_package["review_checklist"] = checklist
    review_package["review_summary"] = _summary(checklist)
    review_package["research_applicability_campaign_plan_review_package_digest"] = (
        research_applicability_campaign_plan_review_package_digest_v1(review_package)
    )
    validate_research_applicability_campaign_plan_candidate_review_package_v1(review_package)
    return review_package


def _reject_forbidden_values(mapping: dict[str, Any], *, path: str = "review_package") -> None:
    for key, value in mapping.items():
        current_path = f"{path}.{key}"
        if isinstance(value, str) and value in {
            "RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTED",
            "PREDICTIVE_USEFULNESS_ACCEPTED",
            "PROFITABILITY_ACCEPTED",
            "RUNTIME_MIGRATION_APPROVED",
            "RUNTIME_MIGRATION_ACTIVE",
            "STRATEGY_RUNTIME_MIGRATION",
        }:
            raise ResearchApplicabilityCampaignPlanOperatorReviewError(
                f"{current_path} must not emit {value}"
            )
        if key in FORBIDDEN_APPROVAL_FIELDS and value is not None:
            raise ResearchApplicabilityCampaignPlanOperatorReviewError(f"{current_path} must be null")
        if key in {
            "campaign_execution_authorized",
            "campaign_execution_performed",
            "runtime_migration_approved",
            "runtime_migration_active",
            "strategy_runtime_migration",
            "automatic_stitching",
            "provider_requests_made_in_review",
            "software_campaign_execution_authorized",
            "software_runtime_migration_authorized",
            "software_runtime_activation_authorized",
        } and value is True:
            raise ResearchApplicabilityCampaignPlanOperatorReviewError(f"{current_path} must be false")
        if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and value == "AUTHORIZED":
            raise ResearchApplicabilityCampaignPlanOperatorReviewError(
                f"{current_path} must not be AUTHORIZED"
            )
        if key in {"predictive_usefulness", "profitability"} and value == "accepted":
            raise ResearchApplicabilityCampaignPlanOperatorReviewError(
                f"{current_path} must not be accepted"
            )
        if isinstance(value, dict):
            _reject_forbidden_values(value, path=current_path)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, dict):
                    _reject_forbidden_values(item, path=f"{current_path}[{index}]")


def _validate_campaign_profiles(review_package: dict[str, Any]) -> None:
    profiles = review_package.get("campaign_profiles")
    if not isinstance(profiles, list) or len(profiles) != 2:
        raise ResearchApplicabilityCampaignPlanOperatorReviewError(
            "campaign_profiles must contain SWING and POSITION_SWING"
        )
    by_profile = _profile_by_name(review_package)
    if "SWING" not in by_profile:
        raise ResearchApplicabilityCampaignPlanOperatorReviewError("missing SWING campaign profile")
    if "POSITION_SWING" not in by_profile:
        raise ResearchApplicabilityCampaignPlanOperatorReviewError(
            "missing POSITION_SWING campaign profile"
        )
    expected_by_profile = {
        profile["dataset_profile"]: profile
        for profile in campaign_plan.build_research_applicability_campaign_plan_candidate_v1()[
            "campaign_profiles"
        ]
    }
    for profile, expected in expected_by_profile.items():
        candidate = by_profile[profile]
        for field, expected_value in expected.items():
            _expect(candidate.get(field), expected_value, field)


def validate_research_applicability_campaign_plan_candidate_review_package_v1(
    review_package: dict[str, Any],
) -> dict[str, Any]:
    """Validate a campaign plan review package without authorizing execution."""
    if not isinstance(review_package, dict):
        raise ResearchApplicabilityCampaignPlanOperatorReviewError(
            "research applicability campaign plan review package must be a JSON object"
        )
    _reject_forbidden_values(review_package)
    _expect(
        review_package.get("artifact_kind"),
        ARTIFACT_KIND_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_CANDIDATE_REVIEW_PACKAGE,
        "artifact_kind",
    )
    _expect(
        review_package.get("schema_version"),
        SCHEMA_VERSION_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_CANDIDATE_REVIEW_V1,
        "schema_version",
    )
    _expect(
        review_package.get("review_status"),
        RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_CANDIDATE_REVIEW_PACKAGE_READY,
        "review_status",
    )
    if review_package.get("binding_mode") not in {
        RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_STATUS_BINDING,
        RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_OBJECT_BINDING,
    }:
        raise ResearchApplicabilityCampaignPlanOperatorReviewError("binding_mode mismatch")
    _expect_true(review_package.get("operator_decision_required"), "operator_decision_required")
    _expect(review_package.get("operator_decision"), None, "operator_decision")
    for field in FORBIDDEN_APPROVAL_FIELDS:
        _expect(review_package.get(field), None, field)
    _expect_true(review_package.get("created_offline"), "created_offline")
    for field in (
        "campaign_execution_authorized",
        "campaign_execution_performed",
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
        _expect(review_package.get(field), campaign_plan.NOT_AUTHORIZED, field)
    _expect(
        review_package.get("predictive_usefulness"),
        acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "predictive_usefulness",
    )
    _expect(review_package.get("profitability"), acquisition.PROFITABILITY_NOT_ACCEPTED, "profitability")
    for field, expected in {
        "reviewed_plan_kind": campaign_plan.ARTIFACT_KIND_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_CANDIDATE,
        "reviewed_plan_status": campaign_plan.RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_READY_FOR_OPERATOR_REVIEW,
        "reviewed_plan_digest": EXPECTED_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_DIGEST,
        "reviewed_plan_checklist_total": EXPECTED_PLAN_CHECKLIST_TOTAL,
        "reviewed_plan_checklist_passed": EXPECTED_PLAN_CHECKLIST_PASSED,
        "reviewed_plan_checklist_failed": EXPECTED_PLAN_CHECKLIST_FAILED,
        "reviewed_plan_blocker_count": EXPECTED_PLAN_BLOCKER_COUNT,
        "campaign_scope": "RESEARCH_ONLY",
        "campaign_ticker_universe": ["AAPL"],
        "campaign_range_start": "2022-01-01",
        "campaign_range_end": "2025-12-31",
        "campaign_touchpoint_inventory_count": 8,
        "campaign_touchpoint_inventory_status": CAMPAIGN_TOUCHPOINT_INVENTORY_INCOMPLETE_COMPACT,
        "dataset_file_availability_verification_review_package_digest": (
            campaign_plan.EXPECTED_DATASET_FILE_AVAILABILITY_VERIFICATION_REVIEW_PACKAGE_DIGEST
        ),
        "dataset_file_availability_verification_package_digest": (
            campaign_plan.EXPECTED_DATASET_FILE_AVAILABILITY_VERIFICATION_PACKAGE_DIGEST
        ),
        "read_only_discovery_review_package_digest": (
            campaign_plan.EXPECTED_READ_ONLY_DISCOVERY_REVIEW_PACKAGE_DIGEST
        ),
        "runtime_migration_review_package_digest": (
            campaign_plan.EXPECTED_RUNTIME_MIGRATION_REVIEW_PACKAGE_DIGEST
        ),
        "swing_registry_approval_digest": (
            campaign_plan.availability_review.verification.discovery.runtime_planning.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST
        ),
        "position_swing_registry_approval_digest": (
            campaign_plan.availability_review.verification.discovery.runtime_planning.EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST
        ),
        "campaign_questions": campaign_plan.CAMPAIGN_QUESTIONS,
        "planned_metrics": campaign_plan.PLANNED_METRICS,
        "planned_outputs": campaign_plan.PLANNED_OUTPUTS,
        "future_execution_gates": campaign_plan.FUTURE_EXECUTION_GATES,
        "risk_controls": campaign_plan.RISK_CONTROLS,
        "remaining_required_tasks": REMAINING_REQUIRED_TASKS,
    }.items():
        _expect(review_package.get(field), expected, field)
    _validate_campaign_profiles(review_package)
    inventory = review_package.get("campaign_touchpoint_inventory")
    if not isinstance(inventory, list) or not inventory:
        raise ResearchApplicabilityCampaignPlanOperatorReviewError("campaign_touchpoint_inventory missing")
    checklist = review_package.get("review_checklist")
    if not isinstance(checklist, list):
        raise ResearchApplicabilityCampaignPlanOperatorReviewError("review_checklist must be a list")
    _expect(
        [item.get("check_id") for item in checklist if isinstance(item, dict)],
        REQUIRED_CHECK_IDS,
        "review_checklist check IDs",
    )
    expected_checklist = _build_checklist(review_package)
    failed = [item for item in expected_checklist if item["status"] != PASS]
    if failed:
        raise ResearchApplicabilityCampaignPlanOperatorReviewError(
            f"research applicability campaign plan review checklist contains failed check: {failed[0]['check_id']}"
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
    digest = review_package.get("research_applicability_campaign_plan_review_package_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise ResearchApplicabilityCampaignPlanOperatorReviewError(
            "research_applicability_campaign_plan_review_package_digest missing"
        )
    _expect(
        digest,
        research_applicability_campaign_plan_review_package_digest_v1(review_package),
        "research_applicability_campaign_plan_review_package_digest",
    )
    return {
        "status": "RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_CANDIDATE_REVIEW_PACKAGE_VALID",
        "artifact_kind": review_package["artifact_kind"],
        "review_status": review_package["review_status"],
        "research_applicability_campaign_plan_review_package_digest": digest,
        "reviewed_plan_digest": EXPECTED_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_DIGEST,
        "dataset_file_availability_verification_review_package_digest": (
            campaign_plan.EXPECTED_DATASET_FILE_AVAILABILITY_VERIFICATION_REVIEW_PACKAGE_DIGEST
        ),
        "swing_registry_approval_digest": review_package["swing_registry_approval_digest"],
        "position_swing_registry_approval_digest": review_package[
            "position_swing_registry_approval_digest"
        ],
        "campaign_scope": "RESEARCH_ONLY",
        "campaign_ticker_universe": ["AAPL"],
        "campaign_profiles": ["SWING", "POSITION_SWING"],
        "total_checks": summary["total_checks"],
        "passed_checks": summary["passed_checks"],
        "failed_checks": summary["failed_checks"],
        "blocker_count": summary["blocker_count"],
        "campaign_execution_authorized": False,
        "campaign_execution_performed": False,
        "runtime_migration_approved": False,
        "runtime_migration_active": False,
        "strategy_runtime_migration": False,
        "runtime_use": campaign_plan.NOT_AUTHORIZED,
        "strategy_use": campaign_plan.NOT_AUTHORIZED,
        "paper_trading": campaign_plan.NOT_AUTHORIZED,
        "broker_execution": campaign_plan.NOT_AUTHORIZED,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
    }


def build_research_applicability_campaign_plan_candidate_review_markdown_v1(
    review_package: dict[str, Any],
) -> str:
    """Render a sanitized research applicability campaign plan review status document."""
    validation = validate_research_applicability_campaign_plan_candidate_review_package_v1(review_package)
    summary = review_package["review_summary"]
    lines = [
        "# MarketFlow Research Applicability Campaign Plan Operator Review Package Status",
        "",
        "## Title",
        "- Research Applicability Campaign Plan Operator Review Package v1.",
        "",
        "## Reviewed Research Applicability Campaign Plan",
        f"- Review package artifact kind: `{review_package['artifact_kind']}`",
        f"- Review status: `{review_package['review_status']}`",
        f"- Binding mode: `{review_package['binding_mode']}`",
        f"- Reviewed plan kind: `{review_package['reviewed_plan_kind']}`",
        f"- Reviewed plan status: `{review_package['reviewed_plan_status']}`",
        f"- Reviewed plan digest: `{review_package['reviewed_plan_digest']}`",
        "",
        "## Campaign Scope",
        f"- Campaign scope: `{review_package['campaign_scope']}`",
        f"- Ticker universe: `{', '.join(review_package['campaign_ticker_universe'])}`",
        f"- Date range: `{review_package['campaign_range_start']}` through `{review_package['campaign_range_end']}`",
        "",
        "## Research Dataset Inputs",
    ]
    for profile in review_package["campaign_profiles"]:
        lines.extend(
            [
                f"- `{profile['registry_key']}`",
                f"  - Registry approval digest: `{profile['registry_approval_digest']}`",
                f"  - Dataset rows digest: `{profile['dataset_rows_digest']}`",
                f"  - Dataset manifest digest: `{profile['dataset_manifest_digest']}`",
                f"  - Runtime use: `{profile['runtime_use']}`",
                f"  - Strategy use: `{profile['strategy_use']}`",
            ]
        )
    lines.extend(["", "## Planned Questions"])
    lines.extend(f"{index}. {question}" for index, question in enumerate(review_package["campaign_questions"], start=1))
    lines.extend(["", "## Planned Metrics"])
    lines.extend(f"- `{metric['name']}`: `{metric['classification']}`" for metric in review_package["planned_metrics"])
    lines.extend(["", "## Future Execution Gates"])
    lines.extend(f"- `{gate}`" for gate in review_package["future_execution_gates"])
    lines.extend(["", "## Risk Controls"])
    lines.extend(f"- {control}" for control in review_package["risk_controls"])
    lines.extend(
        [
            "",
            "## Runtime Boundary",
            f"- campaign_execution_authorized: `{review_package['campaign_execution_authorized']}`",
            f"- campaign_execution_performed: `{review_package['campaign_execution_performed']}`",
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
            "- No Massive.com / Polygon provider data was fetched.",
            "- No walk-forward validation or strategy scoring was run.",
            "- No runtime default source was changed.",
            "- Runtime, Strategy, paper trading, and broker execution use remain `NOT_AUTHORIZED`.",
            "- Predictive usefulness and profitability remain not accepted.",
            "",
            "## Review Package Digest",
            f"- Review package digest: `{validation['research_applicability_campaign_plan_review_package_digest']}`",
            "",
        ]
    )
    return "\n".join(lines)


def write_research_applicability_campaign_plan_candidate_review_package_v1(
    output_dir: str | Path,
    *,
    campaign_plan: dict[str, Any] | None = None,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write the campaign plan review package JSON artifact without overwriting output."""
    review_package = build_research_applicability_campaign_plan_candidate_review_package_v1(
        campaign_plan
    )
    validation = validate_research_applicability_campaign_plan_candidate_review_package_v1(
        review_package
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "research_applicability_campaign_plan_candidate_review_package_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise ResearchApplicabilityCampaignPlanOperatorReviewError(
            "research applicability campaign plan review filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise ResearchApplicabilityCampaignPlanOperatorReviewError(
            "research applicability campaign plan review output already exists"
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
