"""Offline research-only applicability campaign plan candidate."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import dataset_file_availability_verification_operator_review_service as availability_review


ARTIFACT_KIND_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_CANDIDATE = (
    "RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_CANDIDATE"
)
SCHEMA_VERSION_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_CANDIDATE_V1 = (
    "research_applicability_campaign_plan_candidate_v1"
)
RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_READY_FOR_OPERATOR_REVIEW = (
    "RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_READY_FOR_OPERATOR_REVIEW"
)

EXPECTED_DATASET_FILE_AVAILABILITY_VERIFICATION_PACKAGE_DIGEST = (
    availability_review.EXPECTED_DATASET_FILE_AVAILABILITY_VERIFICATION_PACKAGE_DIGEST
)
EXPECTED_DATASET_FILE_AVAILABILITY_VERIFICATION_REVIEW_PACKAGE_DIGEST = (
    "1002c6f19bc57a6537dc71b8a830517de90fbfd89774797a3dd1e9232531ecff"
)
EXPECTED_READ_ONLY_DISCOVERY_CANDIDATE_DIGEST = (
    availability_review.verification.EXPECTED_READ_ONLY_DISCOVERY_CANDIDATE_DIGEST
)
EXPECTED_READ_ONLY_DISCOVERY_REVIEW_PACKAGE_DIGEST = (
    availability_review.verification.EXPECTED_READ_ONLY_DISCOVERY_REVIEW_PACKAGE_DIGEST
)
EXPECTED_RUNTIME_MIGRATION_PLAN_DIGEST = (
    availability_review.verification.discovery.EXPECTED_RUNTIME_MIGRATION_PLAN_DIGEST
)
EXPECTED_RUNTIME_MIGRATION_REVIEW_PACKAGE_DIGEST = (
    availability_review.verification.discovery.EXPECTED_RUNTIME_MIGRATION_REVIEW_PACKAGE_DIGEST
)

NOT_AUTHORIZED = availability_review.verification.NOT_AUTHORIZED
RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE = "RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE"
RESEARCH_ONLY_PLANNED_NOT_CREATED = "RESEARCH_ONLY_PLANNED_NOT_CREATED"

PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
INFO = "INFO"

REQUIRED_CHECK_IDS = [
    "dataset_availability_review_digest_bound",
    "read_only_discovery_review_digest_bound",
    "runtime_migration_review_digest_bound",
    "swing_registry_approval_digest_bound",
    "position_swing_registry_approval_digest_bound",
    "campaign_scope_research_only",
    "campaign_ticker_universe_aapl_only",
    "campaign_profiles_swing_and_position_swing",
    "provider_requests_made_false",
    "campaign_execution_performed_false",
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
    "future_execution_gates_defined",
    "risk_controls_defined",
    "planned_outputs_research_only",
    "campaign_touchpoint_inventory_present",
]

CAMPAIGN_QUESTIONS = [
    "Can existing MarketFlow research modules load the research-registry datasets read-only?",
    "Can SWING and POSITION_SWING datasets pass schema and continuity checks?",
    "Can existing analysis modules compute non-trading descriptive indicators without runtime migration?",
    "Can campaign outputs remain clearly marked research-only and non-actionable?",
    "Which code paths require adaptation before any future runtime migration?",
]

PLANNED_METRICS = [
    {"name": "dataset_load_success", "classification": "RESEARCH_DESCRIPTIVE_ONLY"},
    {"name": "schema_validation_success", "classification": "RESEARCH_DESCRIPTIVE_ONLY"},
    {"name": "bar_count_consistency", "classification": "RESEARCH_DESCRIPTIVE_ONLY"},
    {"name": "date_range_coverage", "classification": "RESEARCH_DESCRIPTIVE_ONLY"},
    {"name": "null_field_summary", "classification": "RESEARCH_DESCRIPTIVE_ONLY"},
    {"name": "OHLC consistency checks", "classification": "RESEARCH_DESCRIPTIVE_ONLY"},
    {"name": "volume consistency checks", "classification": "RESEARCH_DESCRIPTIVE_ONLY"},
    {"name": "indicator_calculation_success", "classification": RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE},
    {"name": "module_compatibility_matrix", "classification": "RESEARCH_DESCRIPTIVE_ONLY"},
    {"name": "failure_reason_inventory", "classification": "RESEARCH_DESCRIPTIVE_ONLY"},
]

PLANNED_OUTPUTS = [
    {"name": "research_campaign_run_manifest", "status": RESEARCH_ONLY_PLANNED_NOT_CREATED},
    {"name": "dataset_load_report", "status": RESEARCH_ONLY_PLANNED_NOT_CREATED},
    {"name": "schema_validation_report", "status": RESEARCH_ONLY_PLANNED_NOT_CREATED},
    {"name": "compatibility_matrix", "status": RESEARCH_ONLY_PLANNED_NOT_CREATED},
    {"name": "failure_inventory", "status": RESEARCH_ONLY_PLANNED_NOT_CREATED},
    {"name": "operator_review_summary", "status": RESEARCH_ONLY_PLANNED_NOT_CREATED},
]

FUTURE_EXECUTION_GATES = [
    "research_campaign_plan_operator_review",
    "research_campaign_execution_approval",
    "read_only_execution_environment_confirmation",
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

EXCLUSION_RULES = [
    "Exclude any ticker other than AAPL unless added by a later authority chain.",
    "Exclude provider refresh or regeneration paths.",
    "Exclude broker, paper-trading, or runtime activation paths.",
    "Exclude final predictive-usefulness or profitability acceptance claims.",
]

NON_GOALS = [
    "No campaign execution.",
    "No walk-forward validation run.",
    "No strategy scoring run.",
    "No provider request.",
    "No generated research campaign outputs.",
    "No runtime migration approval.",
    "No runtime activation.",
    "No paper trading or broker execution.",
    "No predictive-usefulness or profitability acceptance.",
]

REMAINING_REQUIRED_TASKS = [
    "Research applicability campaign plan operator review package.",
    "Research-only applicability campaign execution candidate.",
    "Predictive usefulness review.",
    "Profitability review.",
    "Runtime migration approval ceremony, if ever authorized.",
]


class ResearchApplicabilityCampaignPlanError(ValueError):
    """Raised when a research applicability campaign plan violates guardrails."""


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
        raise ResearchApplicabilityCampaignPlanError(f"{field_name} mismatch")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise ResearchApplicabilityCampaignPlanError(f"{field_name} must be false")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise ResearchApplicabilityCampaignPlanError(f"{field_name} must be true")


def _registry_entry_by_profile(profile: str) -> dict[str, Any]:
    for entry in availability_review.verification.discovery._registry_definitions():
        if entry["dataset_profile"] == profile:
            return entry
    raise ResearchApplicabilityCampaignPlanError(f"{profile} registry entry missing")


def _campaign_profiles() -> list[dict[str, Any]]:
    profiles = []
    for profile in ("SWING", "POSITION_SWING"):
        entry = _registry_entry_by_profile(profile)
        profiles.append(
            {
                "ticker": "AAPL",
                "dataset_profile": entry["dataset_profile"],
                "dataset_bar_rule": entry["dataset_bar_rule"],
                "registry_key": entry["registry_key"],
                "registry_scope": entry["registry_scope"],
                "registry_approval_digest": entry["registry_approval_digest"],
                "dataset_rows_digest": entry["dataset_rows_digest"],
                "dataset_manifest_digest": entry["dataset_manifest_digest"],
                "dataset_file_status": availability_review.verification.AVAILABLE_AND_DIGEST_VERIFIED,
                "manifest_file_status": availability_review.verification.AVAILABLE_AND_DIGEST_VERIFIED,
                "runtime_use": NOT_AUTHORIZED,
                "strategy_use": NOT_AUTHORIZED,
            }
        )
    return profiles


def _campaign_touchpoint_inventory() -> list[dict[str, Any]]:
    return [
        {
            "path": "apps/marketflow_studio.py",
            "role": "Studio",
            "current_behavior_summary": "Local Streamlit interface wires analysis, report, calibration, and validation services.",
            "future_campaign_relevance": "Likely review surface for future campaign controls and research-only output browsing.",
            "risk_level": "medium",
            "recommended_action": "Add explicit research-only campaign controls only after operator approval.",
        },
        {
            "path": "marketflow/services/walk_forward_campaign_service.py",
            "role": "Campaign Aggregator",
            "current_behavior_summary": "Aggregates saved walk-forward CSV artifacts into campaign coverage, summary, and report outputs.",
            "future_campaign_relevance": "Useful for future output aggregation, but not invoked by this plan.",
            "risk_level": "medium",
            "recommended_action": "Require a separate execution candidate before any aggregation run.",
        },
        {
            "path": "marketflow/services/walk_forward_validation_service.py",
            "role": "Walk-Forward Validation",
            "current_behavior_summary": "Builds and evaluates historical walk-forward cases from CSV data.",
            "future_campaign_relevance": "Potential execution engine for a later research-only campaign.",
            "risk_level": "high",
            "recommended_action": "Keep disabled until campaign execution approval and research-only output labeling exist.",
        },
        {
            "path": "marketflow/services/strategy_service.py",
            "role": "strategy candidate generation",
            "current_behavior_summary": "Wraps MarketFlow strategy ranking and report-root source discovery.",
            "future_campaign_relevance": "Possible compatibility target; must not be run for this planning artifact.",
            "risk_level": "high",
            "recommended_action": "Use only in read-only descriptive compatibility checks after explicit execution approval.",
        },
        {
            "path": "marketflow/services/report_index.py",
            "role": "report loading",
            "current_behavior_summary": "Locates and loads generated report folders, JSON reports, and summary text.",
            "future_campaign_relevance": "Can index future research-only campaign artifacts if labeled and isolated.",
            "risk_level": "medium",
            "recommended_action": "Require research-only labels and isolated output paths before use.",
        },
        {
            "path": "marketflow/services/artifact_service.py",
            "role": "artifact classification",
            "current_behavior_summary": "Classifies generated report, CSV, walk-forward, and visualization artifacts.",
            "future_campaign_relevance": "May need campaign artifact classifications after a separate output contract is approved.",
            "risk_level": "medium",
            "recommended_action": "Do not add generated artifact types in this plan-only task.",
        },
        {
            "path": "marketflow/services/data_sufficiency_service.py",
            "role": "dataset loading",
            "current_behavior_summary": "Computes data horizon and sufficiency diagnostics over report folders and CSV artifacts.",
            "future_campaign_relevance": "Candidate source for descriptive data coverage checks.",
            "risk_level": "low",
            "recommended_action": "Limit future use to read-only descriptive diagnostics.",
        },
        {
            "path": "marketflow/__main__.py",
            "role": "CLI entry points",
            "current_behavior_summary": "Runs ticker analysis and report generation commands.",
            "future_campaign_relevance": "Not suitable for this plan because it can invoke analysis/report generation.",
            "risk_level": "high",
            "recommended_action": "Do not route campaign execution through runtime CLI without a separate approval gate.",
        },
    ]


def _plan_context() -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_CANDIDATE,
        "schema_version": SCHEMA_VERSION_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_CANDIDATE_V1,
        "plan_status": RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_READY_FOR_OPERATOR_REVIEW,
        "created_offline": True,
        "provider_requests_made": False,
        "campaign_execution_performed": False,
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
        "campaign_execution_authorized": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
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
    }


def _campaign_scope() -> dict[str, Any]:
    return {
        "scope_type": "RESEARCH_ONLY_APPLICABILITY",
        "ticker": "AAPL",
        "ticker_universe": ["AAPL"],
        "dataset_profiles": ["SWING", "POSITION_SWING"],
        "dataset_bar_rules": ["RTH_HALF_SESSION_195M", "RTH_FULL_SESSION_1D"],
        "date_range": {"start": "2022-01-01", "end": "2025-12-31"},
        "registry_scope": "RESEARCH_DATASET",
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
    }


def _campaign_data_sources(profiles: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "dataset_profile": profile["dataset_profile"],
            "registry_key": profile["registry_key"],
            "dataset_rows_digest": profile["dataset_rows_digest"],
            "dataset_manifest_digest": profile["dataset_manifest_digest"],
            "source_authority": "RESEARCH_REGISTRY_APPROVED_DATASET",
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
        }
        for profile in profiles
    ]


def _profile_by_name(plan: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        profile.get("dataset_profile"): profile
        for profile in plan.get("campaign_profiles") or []
        if isinstance(profile, dict)
    }


def _build_checklist(plan: dict[str, Any]) -> list[dict[str, Any]]:
    profiles = _profile_by_name(plan)
    swing = profiles.get("SWING") or {}
    position = profiles.get("POSITION_SWING") or {}
    return [
        _check(
            "dataset_availability_review_digest_bound",
            EXPECTED_DATASET_FILE_AVAILABILITY_VERIFICATION_REVIEW_PACKAGE_DIGEST,
            plan.get("dataset_file_availability_verification_review_package_digest"),
        ),
        _check(
            "read_only_discovery_review_digest_bound",
            EXPECTED_READ_ONLY_DISCOVERY_REVIEW_PACKAGE_DIGEST,
            plan.get("read_only_discovery_review_package_digest"),
        ),
        _check(
            "runtime_migration_review_digest_bound",
            EXPECTED_RUNTIME_MIGRATION_REVIEW_PACKAGE_DIGEST,
            plan.get("runtime_migration_review_package_digest"),
        ),
        _check(
            "swing_registry_approval_digest_bound",
            availability_review.verification.discovery.runtime_planning.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST,
            swing.get("registry_approval_digest"),
        ),
        _check(
            "position_swing_registry_approval_digest_bound",
            availability_review.verification.discovery.runtime_planning.EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST,
            position.get("registry_approval_digest"),
        ),
        _check("campaign_scope_research_only", True, plan.get("research_only")),
        _check("campaign_ticker_universe_aapl_only", ["AAPL"], plan.get("campaign_ticker_universe")),
        _check(
            "campaign_profiles_swing_and_position_swing",
            ["POSITION_SWING", "SWING"],
            sorted(profiles),
        ),
        _check("provider_requests_made_false", False, plan.get("provider_requests_made")),
        _check("campaign_execution_performed_false", False, plan.get("campaign_execution_performed")),
        _check("runtime_migration_approved_false", False, plan.get("runtime_migration_approved")),
        _check("runtime_migration_active_false", False, plan.get("runtime_migration_active")),
        _check("strategy_runtime_migration_false", False, plan.get("strategy_runtime_migration")),
        _check("runtime_use_not_authorized", NOT_AUTHORIZED, plan.get("runtime_use")),
        _check("strategy_use_not_authorized", NOT_AUTHORIZED, plan.get("strategy_use")),
        _check("paper_trading_not_authorized", NOT_AUTHORIZED, plan.get("paper_trading")),
        _check("broker_execution_not_authorized", NOT_AUTHORIZED, plan.get("broker_execution")),
        _check("automatic_stitching_false", False, plan.get("automatic_stitching")),
        _check(
            "predictive_usefulness_not_accepted",
            acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
            plan.get("predictive_usefulness"),
            severity=INFO,
        ),
        _check(
            "profitability_not_accepted",
            acquisition.PROFITABILITY_NOT_ACCEPTED,
            plan.get("profitability"),
            severity=INFO,
        ),
        _check("future_execution_gates_defined", FUTURE_EXECUTION_GATES, plan.get("operator_gates")),
        _check("risk_controls_defined", RISK_CONTROLS, plan.get("risk_controls")),
        _check(
            "planned_outputs_research_only",
            True,
            all(output.get("status") == RESEARCH_ONLY_PLANNED_NOT_CREATED for output in plan.get("planned_outputs") or []),
        ),
        _check("campaign_touchpoint_inventory_present", True, bool(plan.get("campaign_touchpoint_inventory"))),
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
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def _digest_payload(plan: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(plan)
    payload.pop("research_applicability_campaign_plan_digest", None)
    return payload


def research_applicability_campaign_plan_digest_v1(plan: dict[str, Any]) -> str:
    """Return the deterministic semantic digest for a research campaign plan candidate."""
    return semantic_digest(_digest_payload(plan))


def build_research_applicability_campaign_plan_candidate_v1() -> dict[str, Any]:
    """Build an offline plan candidate without executing the research campaign."""
    profiles = _campaign_profiles()
    plan = {
        **_plan_context(),
        "campaign_name": "AAPL_SWING_POSITION_SWING_RESEARCH_APPLICABILITY_V1",
        "campaign_scope": _campaign_scope(),
        "campaign_profiles": profiles,
        "campaign_ticker_universe": ["AAPL"],
        "campaign_date_range": {"start": "2022-01-01", "end": "2025-12-31"},
        "campaign_data_sources": _campaign_data_sources(profiles),
        "campaign_questions": list(CAMPAIGN_QUESTIONS),
        "planned_metrics": deepcopy(PLANNED_METRICS),
        "planned_outputs": deepcopy(PLANNED_OUTPUTS),
        "exclusion_rules": list(EXCLUSION_RULES),
        "risk_controls": list(RISK_CONTROLS),
        "operator_gates": list(FUTURE_EXECUTION_GATES),
        "non_goals": list(NON_GOALS),
        "campaign_touchpoint_inventory": _campaign_touchpoint_inventory(),
        "campaign_touchpoint_inventory_complete": False,
        "remaining_required_tasks": list(REMAINING_REQUIRED_TASKS),
    }
    checklist = _build_checklist(plan)
    plan["plan_checklist"] = checklist
    plan["plan_summary"] = _summary(checklist)
    plan["research_applicability_campaign_plan_digest"] = research_applicability_campaign_plan_digest_v1(plan)
    validate_research_applicability_campaign_plan_candidate_v1(plan)
    return plan


def _reject_forbidden_values(mapping: dict[str, Any], *, path: str = "plan") -> None:
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
            raise ResearchApplicabilityCampaignPlanError(f"{current_path} must not emit {value}")
        if key in {
            "runtime_migration_approved",
            "runtime_migration_active",
            "strategy_runtime_migration",
            "automatic_stitching",
            "provider_requests_made",
            "campaign_execution_performed",
            "campaign_execution_authorized",
            "runtime_migration_authorized",
            "software_runtime_activation_authorized",
        } and value is True:
            raise ResearchApplicabilityCampaignPlanError(f"{current_path} must be false")
        if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and value == "AUTHORIZED":
            raise ResearchApplicabilityCampaignPlanError(f"{current_path} must not be AUTHORIZED")
        if key in {"predictive_usefulness", "profitability"} and value == "accepted":
            raise ResearchApplicabilityCampaignPlanError(f"{current_path} must not be accepted")
        if isinstance(value, dict):
            _reject_forbidden_values(value, path=current_path)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, dict):
                    _reject_forbidden_values(item, path=f"{current_path}[{index}]")


def _validate_profiles(plan: dict[str, Any]) -> None:
    profiles = plan.get("campaign_profiles")
    if not isinstance(profiles, list) or len(profiles) != 2:
        raise ResearchApplicabilityCampaignPlanError("campaign_profiles must contain SWING and POSITION_SWING")
    by_profile = _profile_by_name(plan)
    if sorted(by_profile) != ["POSITION_SWING", "SWING"]:
        raise ResearchApplicabilityCampaignPlanError("campaign_profiles must include SWING and POSITION_SWING")
    for profile, registry_entry in {
        "SWING": _registry_entry_by_profile("SWING"),
        "POSITION_SWING": _registry_entry_by_profile("POSITION_SWING"),
    }.items():
        candidate = by_profile[profile]
        for field, expected in {
            "ticker": "AAPL",
            "dataset_profile": registry_entry["dataset_profile"],
            "dataset_bar_rule": registry_entry["dataset_bar_rule"],
            "registry_key": registry_entry["registry_key"],
            "registry_scope": "RESEARCH_DATASET",
            "registry_approval_digest": registry_entry["registry_approval_digest"],
            "dataset_rows_digest": registry_entry["dataset_rows_digest"],
            "dataset_manifest_digest": registry_entry["dataset_manifest_digest"],
            "dataset_file_status": availability_review.verification.AVAILABLE_AND_DIGEST_VERIFIED,
            "manifest_file_status": availability_review.verification.AVAILABLE_AND_DIGEST_VERIFIED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
        }.items():
            _expect(candidate.get(field), expected, field)


def _validate_planning_lists(plan: dict[str, Any]) -> None:
    for field, expected in {
        "campaign_questions": CAMPAIGN_QUESTIONS,
        "planned_metrics": PLANNED_METRICS,
        "planned_outputs": PLANNED_OUTPUTS,
        "exclusion_rules": EXCLUSION_RULES,
        "risk_controls": RISK_CONTROLS,
        "operator_gates": FUTURE_EXECUTION_GATES,
        "non_goals": NON_GOALS,
        "remaining_required_tasks": REMAINING_REQUIRED_TASKS,
    }.items():
        _expect(plan.get(field), expected, field)
    inventory = plan.get("campaign_touchpoint_inventory")
    if not isinstance(inventory, list) or not inventory:
        raise ResearchApplicabilityCampaignPlanError("campaign_touchpoint_inventory missing")
    for item in inventory:
        if not isinstance(item, dict):
            raise ResearchApplicabilityCampaignPlanError("campaign_touchpoint_inventory item mismatch")
        for field in (
            "path",
            "role",
            "current_behavior_summary",
            "future_campaign_relevance",
            "risk_level",
            "recommended_action",
        ):
            if not item.get(field):
                raise ResearchApplicabilityCampaignPlanError(f"campaign_touchpoint_inventory {field} missing")


def validate_research_applicability_campaign_plan_candidate_v1(plan: dict[str, Any]) -> dict[str, Any]:
    """Validate a research-only applicability campaign plan without authorizing execution."""
    if not isinstance(plan, dict):
        raise ResearchApplicabilityCampaignPlanError("research applicability campaign plan must be a JSON object")
    _reject_forbidden_values(plan)
    _expect(plan.get("artifact_kind"), ARTIFACT_KIND_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_CANDIDATE, "artifact_kind")
    _expect(
        plan.get("schema_version"),
        SCHEMA_VERSION_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_CANDIDATE_V1,
        "schema_version",
    )
    _expect(
        plan.get("plan_status"),
        RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_READY_FOR_OPERATOR_REVIEW,
        "plan_status",
    )
    for field in ("created_offline", "research_only", "operator_review_required", "campaign_execution_requires_operator_approval"):
        _expect_true(plan.get(field), field)
    for field in (
        "provider_requests_made",
        "campaign_execution_performed",
        "runtime_migration_approved",
        "runtime_migration_active",
        "strategy_runtime_migration",
        "automatic_stitching",
        "campaign_execution_authorized",
        "runtime_migration_authorized",
        "software_runtime_activation_authorized",
        "campaign_touchpoint_inventory_complete",
    ):
        _expect_false(plan.get(field), field)
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(plan.get(field), NOT_AUTHORIZED, field)
    _expect(plan.get("predictive_usefulness"), acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED, "predictive_usefulness")
    _expect(plan.get("profitability"), acquisition.PROFITABILITY_NOT_ACCEPTED, "profitability")
    for field, expected in {
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
        "campaign_name": "AAPL_SWING_POSITION_SWING_RESEARCH_APPLICABILITY_V1",
        "campaign_ticker_universe": ["AAPL"],
        "campaign_date_range": {"start": "2022-01-01", "end": "2025-12-31"},
    }.items():
        _expect(plan.get(field), expected, field)
    _expect(plan.get("campaign_scope"), _campaign_scope(), "campaign_scope")
    _validate_profiles(plan)
    _expect(plan.get("campaign_data_sources"), _campaign_data_sources(plan["campaign_profiles"]), "campaign_data_sources")
    _validate_planning_lists(plan)
    checklist = plan.get("plan_checklist")
    if not isinstance(checklist, list):
        raise ResearchApplicabilityCampaignPlanError("plan_checklist must be a list")
    _expect(
        [item.get("check_id") for item in checklist if isinstance(item, dict)],
        REQUIRED_CHECK_IDS,
        "plan_checklist check IDs",
    )
    expected_checklist = _build_checklist(plan)
    failed = [item for item in expected_checklist if item["status"] != PASS]
    if failed:
        raise ResearchApplicabilityCampaignPlanError(
            f"research applicability campaign plan checklist contains failed check: {failed[0]['check_id']}"
        )
    _expect(checklist, expected_checklist, "plan_checklist")
    summary = _summary(checklist)
    _expect(plan.get("plan_summary"), summary, "plan_summary")
    _expect_true(summary.get("ready_for_operator_review"), "ready_for_operator_review")
    _expect_false(summary.get("campaign_execution_authorized"), "campaign_execution_authorized")
    _expect_false(summary.get("runtime_migration_authorized"), "runtime_migration_authorized")
    _expect_false(summary.get("software_runtime_activation_authorized"), "software_runtime_activation_authorized")
    digest = plan.get("research_applicability_campaign_plan_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise ResearchApplicabilityCampaignPlanError("research_applicability_campaign_plan_digest missing")
    _expect(digest, research_applicability_campaign_plan_digest_v1(plan), "research_applicability_campaign_plan_digest")
    return {
        "status": "RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_CANDIDATE_VALID",
        "artifact_kind": plan["artifact_kind"],
        "plan_status": plan["plan_status"],
        "research_applicability_campaign_plan_digest": digest,
        "dataset_file_availability_verification_review_package_digest": (
            EXPECTED_DATASET_FILE_AVAILABILITY_VERIFICATION_REVIEW_PACKAGE_DIGEST
        ),
        "swing_registry_approval_digest": _registry_entry_by_profile("SWING")["registry_approval_digest"],
        "position_swing_registry_approval_digest": _registry_entry_by_profile("POSITION_SWING")[
            "registry_approval_digest"
        ],
        "campaign_ticker_universe": ["AAPL"],
        "campaign_profiles": ["SWING", "POSITION_SWING"],
        "total_checks": summary["total_checks"],
        "passed_checks": summary["passed_checks"],
        "failed_checks": summary["failed_checks"],
        "blocker_count": summary["blocker_count"],
        "campaign_execution_authorized": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
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


def build_research_applicability_campaign_plan_markdown_v1(plan: dict[str, Any]) -> str:
    """Render a sanitized research applicability campaign plan status document."""
    validation = validate_research_applicability_campaign_plan_candidate_v1(plan)
    summary = plan["plan_summary"]
    lines = [
        "# MarketFlow Research Applicability Campaign Plan Status",
        "",
        "## Title",
        "- Research-Only Applicability Campaign Plan v1.",
        "",
        "## Purpose",
        "- Plan a future research-only applicability campaign without executing it.",
        "- This plan does not approve runtime migration, paper trading, broker execution, predictive usefulness, or profitability.",
        "",
        "## Research Dataset Inputs",
    ]
    for profile in plan["campaign_profiles"]:
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
    lines.extend(
        [
            "",
            "## Campaign Scope",
            f"- Campaign name: `{plan['campaign_name']}`",
            f"- Ticker universe: `{', '.join(plan['campaign_ticker_universe'])}`",
            f"- Date range: `{plan['campaign_date_range']['start']}` through `{plan['campaign_date_range']['end']}`",
            f"- Research only: `{plan['research_only']}`",
            "",
            "## Campaign Questions",
        ]
    )
    lines.extend(f"{index}. {question}" for index, question in enumerate(plan["campaign_questions"], start=1))
    lines.extend(["", "## Planned Metrics"])
    lines.extend(f"- `{metric['name']}`: `{metric['classification']}`" for metric in plan["planned_metrics"])
    lines.extend(["", "## Planned Outputs"])
    lines.extend(f"- `{output['name']}`: `{output['status']}`" for output in plan["planned_outputs"])
    lines.extend(["", "## Future Execution Gates"])
    lines.extend(f"- `{gate}`" for gate in plan["operator_gates"])
    lines.extend(["", "## Risk Controls"])
    lines.extend(f"- {control}" for control in plan["risk_controls"])
    lines.extend(["", "## Campaign Touchpoint Inventory"])
    for item in plan["campaign_touchpoint_inventory"]:
        lines.extend(
            [
                f"- `{item['path']}`",
                f"  - Role: `{item['role']}`",
                f"  - Risk level: `{item['risk_level']}`",
                f"  - Recommended action: {item['recommended_action']}",
            ]
        )
    lines.extend(
        [
            f"- Inventory complete: `{plan['campaign_touchpoint_inventory_complete']}`",
            "",
            "## Checklist Summary",
            f"- Total checks: `{summary['total_checks']}`",
            f"- Passed checks: `{summary['passed_checks']}`",
            f"- Failed checks: `{summary['failed_checks']}`",
            f"- Blocker count: `{summary['blocker_count']}`",
            "",
            "## Runtime Boundary",
            f"- runtime_migration_approved: `{plan['runtime_migration_approved']}`",
            f"- runtime_migration_active: `{plan['runtime_migration_active']}`",
            f"- strategy_runtime_migration: `{plan['strategy_runtime_migration']}`",
            f"- runtime_use: `{plan['runtime_use']}`",
            f"- strategy_use: `{plan['strategy_use']}`",
            f"- paper_trading: `{plan['paper_trading']}`",
            f"- broker_execution: `{plan['broker_execution']}`",
            f"- automatic_stitching: `{plan['automatic_stitching']}`",
            f"- predictive_usefulness: `{plan['predictive_usefulness']}`",
            f"- profitability: `{plan['profitability']}`",
            "",
            "## Non-Goals",
        ]
    )
    lines.extend(f"- {item}" for item in plan["non_goals"])
    lines.extend(
        [
            "",
            "## Plan Digest",
            f"- Plan digest: `{validation['research_applicability_campaign_plan_digest']}`",
            "",
        ]
    )
    return "\n".join(lines)


def write_research_applicability_campaign_plan_candidate_v1(
    output_dir: str | Path,
    *,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write the research applicability campaign plan candidate without overwriting output."""
    plan = build_research_applicability_campaign_plan_candidate_v1()
    validation = validate_research_applicability_campaign_plan_candidate_v1(plan)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "research_applicability_campaign_plan_candidate_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise ResearchApplicabilityCampaignPlanError(
            "research applicability campaign plan filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise ResearchApplicabilityCampaignPlanError(
            "research applicability campaign plan output already exists"
        )
    payload = canonical_json_bytes(plan)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": str(path),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
    }
