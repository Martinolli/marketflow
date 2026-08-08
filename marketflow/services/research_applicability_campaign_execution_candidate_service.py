"""Offline research-only applicability campaign execution candidate."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import research_applicability_campaign_plan_operator_review_service as plan_review


ARTIFACT_KIND_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_CANDIDATE = (
    "RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_CANDIDATE"
)
SCHEMA_VERSION_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_CANDIDATE_V1 = (
    "research_applicability_campaign_execution_candidate_v1"
)
RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_READY_FOR_OPERATOR_REVIEW = (
    "RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_READY_FOR_OPERATOR_REVIEW"
)

EXPECTED_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_DIGEST = (
    plan_review.EXPECTED_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_DIGEST
)
EXPECTED_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_REVIEW_PACKAGE_DIGEST = (
    "e908ef36dc38879ff59a72c2b7260497dfd2e75b1582806ece0b8852416ed01d"
)
EXPECTED_DATASET_FILE_AVAILABILITY_VERIFICATION_PACKAGE_DIGEST = (
    plan_review.campaign_plan.EXPECTED_DATASET_FILE_AVAILABILITY_VERIFICATION_PACKAGE_DIGEST
)
EXPECTED_DATASET_FILE_AVAILABILITY_VERIFICATION_REVIEW_PACKAGE_DIGEST = (
    plan_review.campaign_plan.EXPECTED_DATASET_FILE_AVAILABILITY_VERIFICATION_REVIEW_PACKAGE_DIGEST
)
EXPECTED_READ_ONLY_DISCOVERY_CANDIDATE_DIGEST = (
    plan_review.campaign_plan.EXPECTED_READ_ONLY_DISCOVERY_CANDIDATE_DIGEST
)
EXPECTED_READ_ONLY_DISCOVERY_REVIEW_PACKAGE_DIGEST = (
    plan_review.campaign_plan.EXPECTED_READ_ONLY_DISCOVERY_REVIEW_PACKAGE_DIGEST
)
EXPECTED_RUNTIME_MIGRATION_PLAN_DIGEST = (
    plan_review.campaign_plan.EXPECTED_RUNTIME_MIGRATION_PLAN_DIGEST
)
EXPECTED_RUNTIME_MIGRATION_REVIEW_PACKAGE_DIGEST = (
    plan_review.campaign_plan.EXPECTED_RUNTIME_MIGRATION_REVIEW_PACKAGE_DIGEST
)

NOT_AUTHORIZED = plan_review.campaign_plan.NOT_AUTHORIZED
READ_ONLY_OFFLINE_RESEARCH = "READ_ONLY_OFFLINE_RESEARCH"
NOT_RUNTIME = "NOT_RUNTIME"
NOT_STRATEGY_INPUT = "NOT_STRATEGY_INPUT"
DISABLED = "DISABLED"
RESEARCH_ONLY_NON_ACTIONABLE = "RESEARCH_ONLY_NON_ACTIONABLE"
PLANNED_NOT_GENERATED = "PLANNED_NOT_GENERATED"

PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
INFO = "INFO"

CAMPAIGN_EXECUTION_REQUEST_ID = "AAPL_RESEARCH_APPLICABILITY_EXECUTION_2022_2025_V1"
CAMPAIGN_NAME = "AAPL_SWING_POSITION_SWING_RESEARCH_APPLICABILITY_V1"
PLANNED_OUTPUT_ROOT = ".marketflow/research_applicability_campaigns/AAPL/2022_2025/"
DATE_RANGE_START = "2022-01-01"
DATE_RANGE_END = "2025-12-31"

REQUIRED_CHECK_IDS = [
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
    "planned_outputs_research_only",
    "execution_gates_defined",
    "risk_controls_defined",
    "provider_requests_made_false",
    "campaign_execution_authorized_false",
    "campaign_execution_performed_false",
    "campaign_results_generated_false",
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

PLANNED_OUTPUT_NAMES = [
    "research_campaign_run_manifest",
    "dataset_load_report",
    "schema_validation_report",
    "bar_count_consistency_report",
    "date_range_coverage_report",
    "null_field_summary_report",
    "ohlc_consistency_report",
    "volume_consistency_report",
    "indicator_calculation_report",
    "module_compatibility_matrix",
    "failure_reason_inventory",
    "operator_review_summary",
]

EXECUTION_GATES = [
    "campaign_execution_candidate_operator_review",
    "campaign_execution_operator_approval",
    "read_only_environment_confirmation",
    "dataset_files_still_digest_verified",
    "no_provider_refresh_confirmation",
    "no_broker_execution_confirmation",
    "no_paper_trading_confirmation",
    "no_runtime_default_change_confirmation",
    "output_labeling_research_only_confirmation",
]

RISK_CONTROLS = [
    "no provider refresh",
    "no broker execution",
    "no paper trading",
    "no runtime source switch",
    "no automatic stitching",
    "no trade recommendations",
    "no predictive/profitability acceptance",
    "all outputs labeled research-only",
    "operator approval required before campaign execution",
]

PLANNED_EXECUTION_PHASES = [
    "Load SWING dataset read-only.",
    "Load POSITION_SWING dataset read-only.",
    "Verify schema and digest binding.",
    "Verify date range coverage.",
    "Run descriptive data quality checks.",
    "Run non-trading indicator compatibility checks.",
    "Produce failure inventory.",
    "Produce research-only campaign summary.",
]

NON_GOALS = [
    "No campaign execution.",
    "No walk-forward validation run.",
    "No strategy scoring run.",
    "No provider request.",
    "No acquisition row regeneration.",
    "No SWING or POSITION_SWING bar regeneration.",
    "No runtime migration approval.",
    "No runtime activation.",
    "No paper trading or broker execution.",
    "No predictive-usefulness or profitability acceptance.",
]

REMAINING_REQUIRED_TASKS = [
    "Research applicability campaign execution candidate operator review.",
    "Research-only applicability campaign execution, if approved.",
    "Predictive usefulness review.",
    "Profitability review.",
    "Runtime migration approval ceremony, if ever authorized.",
]


class ResearchApplicabilityCampaignExecutionCandidateError(ValueError):
    """Raised when a research applicability campaign execution candidate violates guardrails."""


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
        raise ResearchApplicabilityCampaignExecutionCandidateError(f"{field_name} mismatch")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise ResearchApplicabilityCampaignExecutionCandidateError(f"{field_name} must be false")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise ResearchApplicabilityCampaignExecutionCandidateError(f"{field_name} must be true")


def _review_package_evidence() -> dict[str, Any]:
    package = plan_review.build_research_applicability_campaign_plan_candidate_review_package_v1()
    try:
        validation = plan_review.validate_research_applicability_campaign_plan_candidate_review_package_v1(package)
    except plan_review.ResearchApplicabilityCampaignPlanOperatorReviewError as exc:
        raise ResearchApplicabilityCampaignExecutionCandidateError(
            f"source research applicability campaign plan review package invalid: {exc}"
        ) from exc
    _expect(
        validation["research_applicability_campaign_plan_review_package_digest"],
        EXPECTED_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_REVIEW_PACKAGE_DIGEST,
        "research_applicability_campaign_plan_review_package_digest",
    )
    return {
        "research_campaign_plan_digest": package["reviewed_plan_digest"],
        "research_campaign_plan_review_package_digest": validation[
            "research_applicability_campaign_plan_review_package_digest"
        ],
        "dataset_file_availability_verification_package_digest": package[
            "dataset_file_availability_verification_package_digest"
        ],
        "dataset_file_availability_verification_review_package_digest": package[
            "dataset_file_availability_verification_review_package_digest"
        ],
        "read_only_discovery_candidate_digest": EXPECTED_READ_ONLY_DISCOVERY_CANDIDATE_DIGEST,
        "read_only_discovery_review_package_digest": package["read_only_discovery_review_package_digest"],
        "runtime_migration_plan_digest": EXPECTED_RUNTIME_MIGRATION_PLAN_DIGEST,
        "runtime_migration_review_package_digest": package["runtime_migration_review_package_digest"],
        "swing_registry_approval_digest": package["swing_registry_approval_digest"],
        "position_swing_registry_approval_digest": package["position_swing_registry_approval_digest"],
        "source_review_package_status": package["review_status"],
        "source_review_checklist_total": validation["total_checks"],
        "source_review_checklist_failed": validation["failed_checks"],
        "campaign_profiles": deepcopy(package["campaign_profiles"]),
    }


def _profile_by_name(candidate: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        profile.get("dataset_profile"): profile
        for profile in candidate.get("planned_inputs") or []
        if isinstance(profile, dict)
    }


def _planned_inputs(campaign_profiles: list[dict[str, Any]]) -> list[dict[str, Any]]:
    inputs = []
    for profile in campaign_profiles:
        dataset_profile = profile["dataset_profile"]
        inputs.append(
            {
                "ticker": "AAPL",
                "dataset_profile": dataset_profile,
                "dataset_bar_rule": profile["dataset_bar_rule"],
                "registry_key": profile["registry_key"],
                "registry_scope": profile["registry_scope"],
                "planned_dataset_path": (
                    ".marketflow/canonical_candidates/AAPL/"
                    f"{dataset_profile}/AAPL_{dataset_profile}_{profile['dataset_bar_rule']}_2022_2025.csv"
                ),
                "registry_approval_digest": profile["registry_approval_digest"],
                "dataset_rows_digest": profile["dataset_rows_digest"],
                "dataset_manifest_digest": profile["dataset_manifest_digest"],
                "runtime_use": NOT_AUTHORIZED,
                "strategy_use": NOT_AUTHORIZED,
                "load_mode": "READ_ONLY",
                "dataset_generation_allowed": False,
                "provider_refresh_allowed": False,
            }
        )
    return inputs


def _campaign_execution_request() -> dict[str, Any]:
    return {
        "campaign_execution_request_id": CAMPAIGN_EXECUTION_REQUEST_ID,
        "campaign_name": CAMPAIGN_NAME,
        "campaign_scope": "RESEARCH_ONLY",
        "ticker_universe": ["AAPL"],
        "dataset_profiles": ["SWING", "POSITION_SWING"],
        "date_range_start": DATE_RANGE_START,
        "date_range_end": DATE_RANGE_END,
        "execution_mode": READ_ONLY_OFFLINE_RESEARCH,
        "runtime_mode": NOT_RUNTIME,
        "strategy_mode": NOT_STRATEGY_INPUT,
        "broker_mode": DISABLED,
        "paper_trading_mode": DISABLED,
    }


def _planned_outputs() -> list[dict[str, Any]]:
    return [
        {
            "name": name,
            "path": f"{PLANNED_OUTPUT_ROOT}{name}.json",
            "status": PLANNED_NOT_GENERATED,
            "generated": False,
            "output_label": RESEARCH_ONLY_NON_ACTIONABLE,
        }
        for name in PLANNED_OUTPUT_NAMES
    ]


def _planned_execution_phases() -> list[dict[str, Any]]:
    return [
        {
            "phase_number": index,
            "action": action,
            "execution_performed": False,
            "output_generated": False,
            "output_label": RESEARCH_ONLY_NON_ACTIONABLE,
        }
        for index, action in enumerate(PLANNED_EXECUTION_PHASES, start=1)
    ]


def _candidate_context() -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_CANDIDATE,
        "schema_version": SCHEMA_VERSION_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_CANDIDATE_V1,
        "candidate_status": RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_READY_FOR_OPERATOR_REVIEW,
        "created_offline": True,
        "provider_requests_made": False,
        "campaign_execution_authorized": False,
        "campaign_execution_performed": False,
        "campaign_results_generated": False,
        "research_only": True,
        "runtime_migration_approved": False,
        "runtime_migration_active": False,
        "strategy_runtime_migration": False,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "automatic_stitching": False,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "operator_review_required": True,
        "campaign_execution_requires_operator_approval": True,
        "software_campaign_execution_authorized": False,
        "software_runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
        "output_label": RESEARCH_ONLY_NON_ACTIONABLE,
    }


def _build_checklist(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    profiles = _profile_by_name(candidate)
    request = candidate.get("campaign_execution_request") or {}
    return [
        _check(
            "campaign_plan_digest_bound",
            EXPECTED_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_DIGEST,
            candidate.get("research_campaign_plan_digest"),
        ),
        _check(
            "campaign_plan_review_digest_bound",
            EXPECTED_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_REVIEW_PACKAGE_DIGEST,
            candidate.get("research_campaign_plan_review_package_digest"),
        ),
        _check(
            "dataset_availability_review_digest_bound",
            EXPECTED_DATASET_FILE_AVAILABILITY_VERIFICATION_REVIEW_PACKAGE_DIGEST,
            candidate.get("dataset_file_availability_verification_review_package_digest"),
        ),
        _check(
            "read_only_discovery_review_digest_bound",
            EXPECTED_READ_ONLY_DISCOVERY_REVIEW_PACKAGE_DIGEST,
            candidate.get("read_only_discovery_review_package_digest"),
        ),
        _check(
            "runtime_migration_review_digest_bound",
            EXPECTED_RUNTIME_MIGRATION_REVIEW_PACKAGE_DIGEST,
            candidate.get("runtime_migration_review_package_digest"),
        ),
        _check(
            "swing_registry_approval_digest_bound",
            plan_review.campaign_plan.availability_review.verification.discovery.runtime_planning.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST,
            candidate.get("swing_registry_approval_digest"),
        ),
        _check(
            "position_swing_registry_approval_digest_bound",
            plan_review.campaign_plan.availability_review.verification.discovery.runtime_planning.EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST,
            candidate.get("position_swing_registry_approval_digest"),
        ),
        _check("campaign_scope_research_only", "RESEARCH_ONLY", request.get("campaign_scope")),
        _check("ticker_universe_aapl_only", ["AAPL"], request.get("ticker_universe")),
        _check("profiles_swing_and_position_swing", ["POSITION_SWING", "SWING"], sorted(profiles)),
        _check(
            "date_range_matches",
            {"start": DATE_RANGE_START, "end": DATE_RANGE_END},
            {"start": request.get("date_range_start"), "end": request.get("date_range_end")},
        ),
        _check("execution_mode_read_only_offline_research", READ_ONLY_OFFLINE_RESEARCH, request.get("execution_mode")),
        _check("runtime_mode_not_runtime", NOT_RUNTIME, request.get("runtime_mode")),
        _check("strategy_mode_not_strategy_input", NOT_STRATEGY_INPUT, request.get("strategy_mode")),
        _check("broker_mode_disabled", DISABLED, request.get("broker_mode")),
        _check("paper_trading_mode_disabled", DISABLED, request.get("paper_trading_mode")),
        _check(
            "planned_outputs_research_only",
            True,
            all(
                output.get("status") == PLANNED_NOT_GENERATED
                and output.get("generated") is False
                and output.get("output_label") == RESEARCH_ONLY_NON_ACTIONABLE
                for output in candidate.get("planned_outputs") or []
            ),
        ),
        _check("execution_gates_defined", EXECUTION_GATES, candidate.get("execution_gates")),
        _check("risk_controls_defined", RISK_CONTROLS, candidate.get("risk_controls")),
        _check("provider_requests_made_false", False, candidate.get("provider_requests_made")),
        _check("campaign_execution_authorized_false", False, candidate.get("campaign_execution_authorized")),
        _check("campaign_execution_performed_false", False, candidate.get("campaign_execution_performed")),
        _check("campaign_results_generated_false", False, candidate.get("campaign_results_generated")),
        _check("runtime_migration_approved_false", False, candidate.get("runtime_migration_approved")),
        _check("runtime_migration_active_false", False, candidate.get("runtime_migration_active")),
        _check("strategy_runtime_migration_false", False, candidate.get("strategy_runtime_migration")),
        _check("runtime_use_not_authorized", NOT_AUTHORIZED, candidate.get("runtime_use")),
        _check("strategy_use_not_authorized", NOT_AUTHORIZED, candidate.get("strategy_use")),
        _check("paper_trading_not_authorized", NOT_AUTHORIZED, candidate.get("paper_trading")),
        _check("broker_execution_not_authorized", NOT_AUTHORIZED, candidate.get("broker_execution")),
        _check("automatic_stitching_false", False, candidate.get("automatic_stitching")),
        _check(
            "predictive_usefulness_not_accepted",
            acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
            candidate.get("predictive_usefulness"),
            severity=INFO,
        ),
        _check(
            "profitability_not_accepted",
            acquisition.PROFITABILITY_NOT_ACCEPTED,
            candidate.get("profitability"),
            severity=INFO,
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
        "ready_for_operator_review": failed == 0,
        "campaign_execution_authorized": False,
        "campaign_execution_performed": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def _digest_payload(candidate: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(candidate)
    payload.pop("research_applicability_campaign_execution_candidate_digest", None)
    return payload


def research_applicability_campaign_execution_candidate_digest_v1(candidate: dict[str, Any]) -> str:
    """Return the deterministic semantic digest for a research campaign execution candidate."""
    return semantic_digest(_digest_payload(candidate))


def build_research_applicability_campaign_execution_candidate_v1() -> dict[str, Any]:
    """Build an offline candidate for operator review without executing the campaign."""
    evidence = _review_package_evidence()
    planned_inputs = _planned_inputs(evidence.pop("campaign_profiles"))
    request = _campaign_execution_request()
    candidate = {
        **_candidate_context(),
        **request,
        **evidence,
        "campaign_execution_request": request,
        "planned_inputs": planned_inputs,
        "planned_output_root": PLANNED_OUTPUT_ROOT,
        "planned_outputs": _planned_outputs(),
        "planned_execution_phases": _planned_execution_phases(),
        "execution_gates": list(EXECUTION_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "non_goals": list(NON_GOALS),
        "remaining_required_tasks": list(REMAINING_REQUIRED_TASKS),
    }
    checklist = _build_checklist(candidate)
    candidate["candidate_checklist"] = checklist
    candidate["candidate_summary"] = _summary(checklist)
    candidate["research_applicability_campaign_execution_candidate_digest"] = (
        research_applicability_campaign_execution_candidate_digest_v1(candidate)
    )
    validate_research_applicability_campaign_execution_candidate_v1(candidate)
    return candidate


def _reject_forbidden_values(mapping: dict[str, Any], *, path: str = "candidate") -> None:
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
            "STRATEGY_RUNTIME_MIGRATION_ACTIVE",
        }:
            raise ResearchApplicabilityCampaignExecutionCandidateError(
                f"{current_path} must not emit {value}"
            )
        if key in {
            "provider_requests_made",
            "campaign_execution_authorized",
            "campaign_execution_performed",
            "campaign_results_generated",
            "runtime_migration_approved",
            "runtime_migration_active",
            "strategy_runtime_migration",
            "automatic_stitching",
            "software_campaign_execution_authorized",
            "software_runtime_migration_authorized",
            "software_runtime_activation_authorized",
            "dataset_generation_allowed",
            "provider_refresh_allowed",
            "execution_performed",
            "output_generated",
            "generated",
        } and value is True:
            raise ResearchApplicabilityCampaignExecutionCandidateError(f"{current_path} must be false")
        if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and value == "AUTHORIZED":
            raise ResearchApplicabilityCampaignExecutionCandidateError(
                f"{current_path} must not be AUTHORIZED"
            )
        if key in {"predictive_usefulness", "profitability"} and value == "accepted":
            raise ResearchApplicabilityCampaignExecutionCandidateError(
                f"{current_path} must not be accepted"
            )
        if isinstance(value, dict):
            _reject_forbidden_values(value, path=current_path)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, dict):
                    _reject_forbidden_values(item, path=f"{current_path}[{index}]")


def _validate_request(candidate: dict[str, Any]) -> None:
    request = candidate.get("campaign_execution_request")
    if not isinstance(request, dict):
        raise ResearchApplicabilityCampaignExecutionCandidateError("campaign_execution_request missing")
    expected = _campaign_execution_request()
    _expect(request, expected, "campaign_execution_request")
    for field, expected_value in expected.items():
        _expect(candidate.get(field), expected_value, field)


def _validate_planned_inputs(candidate: dict[str, Any]) -> None:
    planned_inputs = candidate.get("planned_inputs")
    if not isinstance(planned_inputs, list) or len(planned_inputs) != 2:
        raise ResearchApplicabilityCampaignExecutionCandidateError(
            "planned_inputs must contain SWING and POSITION_SWING"
        )
    by_profile = _profile_by_name(candidate)
    if sorted(by_profile) != ["POSITION_SWING", "SWING"]:
        raise ResearchApplicabilityCampaignExecutionCandidateError(
            "planned_inputs must include SWING and POSITION_SWING"
        )
    expected_inputs = {
        item["dataset_profile"]: item
        for item in _planned_inputs(
            plan_review.build_research_applicability_campaign_plan_candidate_review_package_v1()[
                "campaign_profiles"
            ]
        )
    }
    for profile, expected in expected_inputs.items():
        candidate_profile = by_profile[profile]
        for field, expected_value in expected.items():
            _expect(candidate_profile.get(field), expected_value, field)


def _validate_planning_lists(candidate: dict[str, Any]) -> None:
    _expect(candidate.get("planned_output_root"), PLANNED_OUTPUT_ROOT, "planned_output_root")
    _expect(candidate.get("planned_outputs"), _planned_outputs(), "planned_outputs")
    _expect(
        candidate.get("planned_execution_phases"),
        _planned_execution_phases(),
        "planned_execution_phases",
    )
    _expect(candidate.get("execution_gates"), EXECUTION_GATES, "execution_gates")
    _expect(candidate.get("risk_controls"), RISK_CONTROLS, "risk_controls")
    _expect(candidate.get("non_goals"), NON_GOALS, "non_goals")
    _expect(candidate.get("remaining_required_tasks"), REMAINING_REQUIRED_TASKS, "remaining_required_tasks")


def validate_research_applicability_campaign_execution_candidate_v1(
    candidate: dict[str, Any],
) -> dict[str, Any]:
    """Validate an execution candidate without authorizing or performing campaign execution."""
    if not isinstance(candidate, dict):
        raise ResearchApplicabilityCampaignExecutionCandidateError(
            "research applicability campaign execution candidate must be a JSON object"
        )
    _reject_forbidden_values(candidate)
    _expect(
        candidate.get("artifact_kind"),
        ARTIFACT_KIND_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_CANDIDATE,
        "artifact_kind",
    )
    _expect(
        candidate.get("schema_version"),
        SCHEMA_VERSION_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_CANDIDATE_V1,
        "schema_version",
    )
    _expect(
        candidate.get("candidate_status"),
        RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_READY_FOR_OPERATOR_REVIEW,
        "candidate_status",
    )
    for field in ("created_offline", "research_only", "operator_review_required", "campaign_execution_requires_operator_approval"):
        _expect_true(candidate.get(field), field)
    for field in (
        "provider_requests_made",
        "campaign_execution_authorized",
        "campaign_execution_performed",
        "campaign_results_generated",
        "runtime_migration_approved",
        "runtime_migration_active",
        "strategy_runtime_migration",
        "automatic_stitching",
        "software_campaign_execution_authorized",
        "software_runtime_migration_authorized",
        "software_runtime_activation_authorized",
    ):
        _expect_false(candidate.get(field), field)
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(candidate.get(field), NOT_AUTHORIZED, field)
    _expect(candidate.get("predictive_usefulness"), acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED, "predictive_usefulness")
    _expect(candidate.get("profitability"), acquisition.PROFITABILITY_NOT_ACCEPTED, "profitability")
    _expect(candidate.get("output_label"), RESEARCH_ONLY_NON_ACTIONABLE, "output_label")
    for field, expected in {
        "research_campaign_plan_digest": EXPECTED_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_DIGEST,
        "research_campaign_plan_review_package_digest": (
            EXPECTED_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_REVIEW_PACKAGE_DIGEST
        ),
        "dataset_file_availability_verification_package_digest": (
            EXPECTED_DATASET_FILE_AVAILABILITY_VERIFICATION_PACKAGE_DIGEST
        ),
        "dataset_file_availability_verification_review_package_digest": (
            EXPECTED_DATASET_FILE_AVAILABILITY_VERIFICATION_REVIEW_PACKAGE_DIGEST
        ),
        "read_only_discovery_candidate_digest": EXPECTED_READ_ONLY_DISCOVERY_CANDIDATE_DIGEST,
        "read_only_discovery_review_package_digest": EXPECTED_READ_ONLY_DISCOVERY_REVIEW_PACKAGE_DIGEST,
        "runtime_migration_plan_digest": EXPECTED_RUNTIME_MIGRATION_PLAN_DIGEST,
        "runtime_migration_review_package_digest": EXPECTED_RUNTIME_MIGRATION_REVIEW_PACKAGE_DIGEST,
        "swing_registry_approval_digest": (
            plan_review.campaign_plan.availability_review.verification.discovery.runtime_planning.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST
        ),
        "position_swing_registry_approval_digest": (
            plan_review.campaign_plan.availability_review.verification.discovery.runtime_planning.EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST
        ),
        "source_review_package_status": (
            plan_review.RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_CANDIDATE_REVIEW_PACKAGE_READY
        ),
        "source_review_checklist_total": len(plan_review.REQUIRED_CHECK_IDS),
        "source_review_checklist_failed": 0,
    }.items():
        _expect(candidate.get(field), expected, field)
    _validate_request(candidate)
    _validate_planned_inputs(candidate)
    _validate_planning_lists(candidate)
    checklist = candidate.get("candidate_checklist")
    if not isinstance(checklist, list):
        raise ResearchApplicabilityCampaignExecutionCandidateError("candidate_checklist must be a list")
    _expect(
        [item.get("check_id") for item in checklist if isinstance(item, dict)],
        REQUIRED_CHECK_IDS,
        "candidate_checklist check IDs",
    )
    expected_checklist = _build_checklist(candidate)
    failed = [item for item in expected_checklist if item["status"] != PASS]
    if failed:
        raise ResearchApplicabilityCampaignExecutionCandidateError(
            f"research applicability campaign execution candidate checklist contains failed check: {failed[0]['check_id']}"
        )
    _expect(checklist, expected_checklist, "candidate_checklist")
    summary = _summary(checklist)
    _expect(candidate.get("candidate_summary"), summary, "candidate_summary")
    _expect_true(summary.get("ready_for_operator_review"), "ready_for_operator_review")
    _expect_false(summary.get("campaign_execution_authorized"), "campaign_execution_authorized")
    _expect_false(summary.get("campaign_execution_performed"), "campaign_execution_performed")
    _expect_false(summary.get("runtime_migration_authorized"), "runtime_migration_authorized")
    _expect_false(summary.get("software_runtime_activation_authorized"), "software_runtime_activation_authorized")
    digest = candidate.get("research_applicability_campaign_execution_candidate_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise ResearchApplicabilityCampaignExecutionCandidateError(
            "research_applicability_campaign_execution_candidate_digest missing"
        )
    _expect(
        digest,
        research_applicability_campaign_execution_candidate_digest_v1(candidate),
        "research_applicability_campaign_execution_candidate_digest",
    )
    return {
        "status": "RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_CANDIDATE_VALID",
        "artifact_kind": candidate["artifact_kind"],
        "candidate_status": candidate["candidate_status"],
        "campaign_execution_request_id": candidate["campaign_execution_request_id"],
        "research_applicability_campaign_execution_candidate_digest": digest,
        "research_campaign_plan_digest": EXPECTED_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_DIGEST,
        "research_campaign_plan_review_package_digest": (
            EXPECTED_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_REVIEW_PACKAGE_DIGEST
        ),
        "dataset_file_availability_verification_review_package_digest": (
            EXPECTED_DATASET_FILE_AVAILABILITY_VERIFICATION_REVIEW_PACKAGE_DIGEST
        ),
        "swing_registry_approval_digest": candidate["swing_registry_approval_digest"],
        "position_swing_registry_approval_digest": candidate[
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
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
    }


def build_research_applicability_campaign_execution_candidate_markdown_v1(
    candidate: dict[str, Any],
) -> str:
    """Render a sanitized research applicability campaign execution candidate status document."""
    validation = validate_research_applicability_campaign_execution_candidate_v1(candidate)
    summary = candidate["candidate_summary"]
    lines = [
        "# MarketFlow Research Applicability Campaign Execution Candidate Status",
        "",
        "## Title",
        "- Research-Only Applicability Campaign Execution Candidate v1.",
        "",
        "## Candidate",
        f"- Artifact kind: `{candidate['artifact_kind']}`",
        f"- Candidate status: `{candidate['candidate_status']}`",
        f"- Campaign execution request ID: `{candidate['campaign_execution_request_id']}`",
        f"- Execution mode: `{candidate['execution_mode']}`",
        f"- Output label: `{candidate['output_label']}`",
        "",
        "## Bound Source Evidence",
        f"- Campaign plan digest: `{candidate['research_campaign_plan_digest']}`",
        f"- Campaign plan review package digest: `{candidate['research_campaign_plan_review_package_digest']}`",
        f"- Dataset availability review digest: `{candidate['dataset_file_availability_verification_review_package_digest']}`",
        f"- Read-only discovery review digest: `{candidate['read_only_discovery_review_package_digest']}`",
        f"- Runtime migration review digest: `{candidate['runtime_migration_review_package_digest']}`",
        f"- SWING registry approval digest: `{candidate['swing_registry_approval_digest']}`",
        f"- POSITION_SWING registry approval digest: `{candidate['position_swing_registry_approval_digest']}`",
        "",
        "## Campaign Scope",
        f"- Campaign name: `{candidate['campaign_name']}`",
        f"- Ticker universe: `{', '.join(candidate['ticker_universe'])}`",
        f"- Dataset profiles: `{', '.join(candidate['dataset_profiles'])}`",
        f"- Date range: `{candidate['date_range_start']}` through `{candidate['date_range_end']}`",
        f"- Runtime mode: `{candidate['runtime_mode']}`",
        f"- Strategy mode: `{candidate['strategy_mode']}`",
        "",
        "## Planned Inputs",
    ]
    for profile in candidate["planned_inputs"]:
        lines.extend(
            [
                f"- `{profile['registry_key']}`",
                f"  - Planned dataset path: `{profile['planned_dataset_path']}`",
                f"  - Registry approval digest: `{profile['registry_approval_digest']}`",
                f"  - Dataset rows digest: `{profile['dataset_rows_digest']}`",
                f"  - Dataset manifest digest: `{profile['dataset_manifest_digest']}`",
                f"  - Runtime use: `{profile['runtime_use']}`",
                f"  - Strategy use: `{profile['strategy_use']}`",
            ]
        )
    lines.extend(["", "## Planned Outputs", f"- Planned output root: `{candidate['planned_output_root']}`"])
    lines.extend(
        f"- `{output['name']}`: `{output['status']}` / generated `{output['generated']}` / label `{output['output_label']}`"
        for output in candidate["planned_outputs"]
    )
    lines.extend(["", "## Planned Execution Phases"])
    lines.extend(
        f"{phase['phase_number']}. {phase['action']} Execution performed: `{phase['execution_performed']}`."
        for phase in candidate["planned_execution_phases"]
    )
    lines.extend(["", "## Execution Gates"])
    lines.extend(f"- `{gate}`" for gate in candidate["execution_gates"])
    lines.extend(["", "## Risk Controls"])
    lines.extend(f"- {control}" for control in candidate["risk_controls"])
    lines.extend(
        [
            "",
            "## Runtime Boundary",
            f"- provider_requests_made: `{candidate['provider_requests_made']}`",
            f"- campaign_execution_authorized: `{candidate['campaign_execution_authorized']}`",
            f"- campaign_execution_performed: `{candidate['campaign_execution_performed']}`",
            f"- campaign_results_generated: `{candidate['campaign_results_generated']}`",
            f"- runtime_migration_approved: `{candidate['runtime_migration_approved']}`",
            f"- runtime_migration_active: `{candidate['runtime_migration_active']}`",
            f"- strategy_runtime_migration: `{candidate['strategy_runtime_migration']}`",
            f"- runtime_use: `{candidate['runtime_use']}`",
            f"- strategy_use: `{candidate['strategy_use']}`",
            f"- paper_trading: `{candidate['paper_trading']}`",
            f"- broker_execution: `{candidate['broker_execution']}`",
            f"- automatic_stitching: `{candidate['automatic_stitching']}`",
            f"- predictive_usefulness: `{candidate['predictive_usefulness']}`",
            f"- profitability: `{candidate['profitability']}`",
            "",
            "## Checklist Summary",
            f"- Total checks: `{summary['total_checks']}`",
            f"- Passed checks: `{summary['passed_checks']}`",
            f"- Failed checks: `{summary['failed_checks']}`",
            f"- Blocker count: `{summary['blocker_count']}`",
            "",
            "## Non-Goals",
        ]
    )
    lines.extend(f"- {item}" for item in candidate["non_goals"])
    lines.extend(
        [
            "",
            "## Candidate Digest",
            f"- Candidate digest: `{validation['research_applicability_campaign_execution_candidate_digest']}`",
            "",
        ]
    )
    return "\n".join(lines)


def write_research_applicability_campaign_execution_candidate_v1(
    output_dir: str | Path,
    *,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write the campaign execution candidate JSON artifact without overwriting output."""
    candidate = build_research_applicability_campaign_execution_candidate_v1()
    validation = validate_research_applicability_campaign_execution_candidate_v1(candidate)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "research_applicability_campaign_execution_candidate_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise ResearchApplicabilityCampaignExecutionCandidateError(
            "research applicability campaign execution candidate filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise ResearchApplicabilityCampaignExecutionCandidateError(
            "research applicability campaign execution candidate output already exists"
        )
    payload = canonical_json_bytes(candidate)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": str(path),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
    }
