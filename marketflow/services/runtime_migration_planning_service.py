"""Offline runtime migration planning candidate helpers."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import position_swing_registry_approval_ceremony_service as position_approval
from marketflow.services import position_swing_registry_approval_service as position_registry
from marketflow.services import swing_registry_approval_ceremony_service as swing_approval
from marketflow.services import swing_registry_approval_service as swing_registry


ARTIFACT_KIND_RUNTIME_MIGRATION_PLAN_CANDIDATE = "RUNTIME_MIGRATION_PLAN_CANDIDATE"
SCHEMA_VERSION_RUNTIME_MIGRATION_PLAN_CANDIDATE_V1 = "runtime_migration_plan_candidate_v1"
RUNTIME_MIGRATION_PLAN_READY_FOR_OPERATOR_REVIEW = "RUNTIME_MIGRATION_PLAN_READY_FOR_OPERATOR_REVIEW"

EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST = "ee3f6b193a6480fb6391fd97b096dda8fc699d65e43a179c77bba8798f887761"
EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST = (
    "8eefcbc1e14b2e199dadd8dcf461cbff56513f10758b6b59ca8cf176512d2e8e"
)
NOT_AUTHORIZED = "NOT_AUTHORIZED"

PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
INFO = "INFO"

PLANNED_PHASES = [
    "Read-only registry discovery service.",
    "Dataset manifest locator.",
    "Dataset file availability verification.",
    "Strategy/Studio read-only display integration.",
    "Research-only applicability campaign runner.",
    "Operator review of research campaign results.",
    "Separate runtime migration approval ceremony, if ever authorized.",
]

FUTURE_GATES = [
    "read_only_registry_discovery_review",
    "dataset_file_availability_review",
    "research_campaign_plan_review",
    "applicability_campaign_completion",
    "predictive_usefulness_review",
    "profitability_review",
    "runtime_migration_operator_approval",
]

HARD_GUARDRAILS = [
    "no runtime default change",
    "no automatic strategy input replacement",
    "no paper trading",
    "no broker execution",
    "no predictive claim",
    "no profitability claim",
    "no automatic stitching",
    "no silent fallback to non-authorized datasets",
]

REMAINING_ROADMAP = [
    "Runtime migration operator review package.",
    "Read-only registry discovery candidate.",
    "Dataset availability verification.",
    "Research-only applicability campaign plan.",
]

REQUIRED_CHECK_IDS = [
    "swing_registry_approval_digest_bound",
    "position_swing_registry_approval_digest_bound",
    "swing_registry_scope_research_dataset",
    "position_swing_registry_scope_research_dataset",
    "swing_runtime_use_not_authorized",
    "position_swing_runtime_use_not_authorized",
    "swing_strategy_use_not_authorized",
    "position_swing_strategy_use_not_authorized",
    "identity_authority_bound",
    "calendar_authority_bound",
    "split_authority_bound",
    "dividend_authority_bound",
    "acquisition_authority_bound",
    "runtime_migration_approved_false",
    "runtime_migration_active_false",
    "strategy_runtime_migration_false",
    "automatic_stitching_false",
    "paper_trading_not_authorized",
    "broker_execution_not_authorized",
    "predictive_usefulness_not_accepted",
    "profitability_not_accepted",
    "runtime_touchpoint_inventory_present",
    "future_gates_defined",
    "hard_guardrails_defined",
]


class RuntimeMigrationPlanningError(ValueError):
    """Raised when a runtime migration plan violates planning guardrails."""


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
        raise RuntimeMigrationPlanningError(f"{field_name} mismatch")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise RuntimeMigrationPlanningError(f"{field_name} must be false")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise RuntimeMigrationPlanningError(f"{field_name} must be true")


def _authority_digests() -> dict[str, Any]:
    return {
        "identity_frozen_digest": acquisition.EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST,
        "calendar_frozen_digest": acquisition.EXPECTED_EXCHANGE_CALENDAR_FROZEN_DIGEST,
        "schedule_digest": acquisition.EXPECTED_SCHEDULE_SEMANTIC_DIGEST,
        "split_event_frozen_digest": acquisition.EXPECTED_SPLIT_EVENT_AUDIT_FROZEN_DIGEST,
        "dividend_event_frozen_digest": acquisition.EXPECTED_DIVIDEND_EVENT_AUDIT_FROZEN_DIGEST,
        "acquisition_generation_frozen_digest": swing_registry.EXPECTED_ACQUISITION_GENERATION_FROZEN_DIGEST,
    }


def _runtime_touchpoint_inventory() -> list[dict[str, Any]]:
    return [
        {
            "path": "marketflow/__main__.py",
            "role": "CLI entry point",
            "current_behavior_summary": "Runs normal fixed-profile orchestration or ad hoc analysis/report generation.",
            "future_migration_relevance": "Would need explicit read-only registry discovery commands before any runtime approval path.",
            "risk_level": "high",
            "recommended_action": "Do not change commands in this planning step; add a future read-only discovery command behind review.",
        },
        {
            "path": "apps/marketflow_studio.py",
            "role": "Studio UI",
            "current_behavior_summary": "Loads reports, runs analysis, ranks strategies, and displays generated artifacts.",
            "future_migration_relevance": "Candidate location for read-only registry and dataset availability display.",
            "risk_level": "high",
            "recommended_action": "Limit any future integration to display-only registry state until runtime approval exists.",
        },
        {
            "path": "marketflow/services/strategy_service.py",
            "role": "Strategy Ranking service",
            "current_behavior_summary": "Discovers report folders and ranks candidates from existing report and CSV inputs.",
            "future_migration_relevance": "Must not silently replace current Strategy inputs with registry datasets.",
            "risk_level": "high",
            "recommended_action": "Require an explicit locator and operator-reviewed source identity before integration.",
        },
        {
            "path": "marketflow/services/artifact_service.py",
            "role": "Generated artifact discovery and preview",
            "current_behavior_summary": "Classifies report artifacts by filename and extension for display/download.",
            "future_migration_relevance": "May need read-only classification for registry and migration planning artifacts.",
            "risk_level": "medium",
            "recommended_action": "Add classification only after operator review of artifact naming and display behavior.",
        },
        {
            "path": "marketflow/services/walk_forward_validation_service.py",
            "role": "Walk-forward validation builder/evaluator",
            "current_behavior_summary": "Builds deterministic walk-forward cases from supplied CSV rows.",
            "future_migration_relevance": "Likely runner for research-only applicability campaigns after dataset availability checks.",
            "risk_level": "medium",
            "recommended_action": "Keep research-only and require explicit dataset identity binding.",
        },
        {
            "path": "marketflow/services/walk_forward_campaign_service.py",
            "role": "Walk-forward campaign aggregator",
            "current_behavior_summary": "Aggregates saved validation artifacts and coverage outputs.",
            "future_migration_relevance": "Could summarize applicability campaign outputs before any runtime migration review.",
            "risk_level": "medium",
            "recommended_action": "Use only after a separate research campaign plan and run registry review.",
        },
        {
            "path": "marketflow/services/walk_forward_run_registry_service.py",
            "role": "Saved walk-forward run registry",
            "current_behavior_summary": "Writes and refreshes metadata for saved walk-forward validation artifacts.",
            "future_migration_relevance": "May hold read-only campaign evidence; not a runtime dataset registry.",
            "risk_level": "medium",
            "recommended_action": "Do not conflate campaign run registry with approved dataset registry.",
        },
        {
            "path": "marketflow/marketflow_data_provider.py",
            "role": "Historical market data provider",
            "current_behavior_summary": "Contains Polygon/Massive provider access and relative-period fetch behavior.",
            "future_migration_relevance": "Provider calls are outside runtime migration planning and must remain disabled here.",
            "risk_level": "high",
            "recommended_action": "Do not call or modify provider paths in migration planning.",
        },
        {
            "path": "marketflow/services/acquisition_provider_adapter_service.py",
            "role": "Live acquisition provider adapter",
            "current_behavior_summary": "Builds and executes gated live Massive.com custom-bars requests.",
            "future_migration_relevance": "No future runtime migration step should refresh source authority through this path implicitly.",
            "risk_level": "high",
            "recommended_action": "Keep provider execution separated behind existing gates and outside default tests.",
        },
        {
            "path": "marketflow/operational_artifacts.py",
            "role": "Operational artifact lineage helpers",
            "current_behavior_summary": "Commits immutable operational artifacts and manifests for analysis workflows.",
            "future_migration_relevance": "May inform future immutable runtime migration evidence packaging.",
            "risk_level": "medium",
            "recommended_action": "Reuse lineage style only after defining a separate migration approval artifact contract.",
        },
    ]


def _registry_inputs() -> dict[str, Any]:
    return {
        "swing_registry_approved": True,
        "swing_registry_approval_digest": EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST,
        "swing_registry_key": swing_registry.PROPOSED_REGISTRY_KEY,
        "swing_registry_scope": swing_registry.PROPOSED_REGISTRY_SCOPE,
        "swing_runtime_use": swing_registry.NOT_AUTHORIZED,
        "swing_strategy_use": swing_registry.NOT_AUTHORIZED,
        "swing_dataset_rows_digest": swing_registry.EXPECTED_DATASET_ROWS_DIGEST,
        "swing_dataset_manifest_digest": swing_registry.EXPECTED_DATASET_MANIFEST_DIGEST,
        "swing_bar_count": swing_registry.EXPECTED_SWING_BAR_COUNT,
        "position_swing_registry_approved": True,
        "position_swing_registry_approval_digest": EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST,
        "position_swing_registry_key": position_registry.PROPOSED_REGISTRY_KEY,
        "position_swing_registry_scope": position_registry.PROPOSED_REGISTRY_SCOPE,
        "position_swing_runtime_use": position_registry.NOT_AUTHORIZED,
        "position_swing_strategy_use": position_registry.NOT_AUTHORIZED,
        "position_swing_dataset_rows_digest": position_registry.EXPECTED_DATASET_ROWS_DIGEST,
        "position_swing_dataset_manifest_digest": position_registry.EXPECTED_DATASET_MANIFEST_DIGEST,
        "position_swing_bar_count": position_registry.EXPECTED_POSITION_SWING_BAR_COUNT,
    }


def _build_checklist(plan: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        _check("swing_registry_approval_digest_bound", EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST, plan.get("swing_registry_approval_digest")),
        _check("position_swing_registry_approval_digest_bound", EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST, plan.get("position_swing_registry_approval_digest")),
        _check("swing_registry_scope_research_dataset", swing_registry.PROPOSED_REGISTRY_SCOPE, plan.get("swing_registry_scope")),
        _check("position_swing_registry_scope_research_dataset", position_registry.PROPOSED_REGISTRY_SCOPE, plan.get("position_swing_registry_scope")),
        _check("swing_runtime_use_not_authorized", NOT_AUTHORIZED, plan.get("swing_runtime_use")),
        _check("position_swing_runtime_use_not_authorized", NOT_AUTHORIZED, plan.get("position_swing_runtime_use")),
        _check("swing_strategy_use_not_authorized", NOT_AUTHORIZED, plan.get("swing_strategy_use")),
        _check("position_swing_strategy_use_not_authorized", NOT_AUTHORIZED, plan.get("position_swing_strategy_use")),
        _check("identity_authority_bound", acquisition.EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST, plan.get("identity_frozen_digest")),
        _check("calendar_authority_bound", acquisition.EXPECTED_EXCHANGE_CALENDAR_FROZEN_DIGEST, plan.get("calendar_frozen_digest")),
        _check("split_authority_bound", acquisition.EXPECTED_SPLIT_EVENT_AUDIT_FROZEN_DIGEST, plan.get("split_event_frozen_digest")),
        _check("dividend_authority_bound", acquisition.EXPECTED_DIVIDEND_EVENT_AUDIT_FROZEN_DIGEST, plan.get("dividend_event_frozen_digest")),
        _check("acquisition_authority_bound", swing_registry.EXPECTED_ACQUISITION_GENERATION_FROZEN_DIGEST, plan.get("acquisition_generation_frozen_digest")),
        _check("runtime_migration_approved_false", False, plan.get("runtime_migration_approved")),
        _check("runtime_migration_active_false", False, plan.get("runtime_migration_active")),
        _check("strategy_runtime_migration_false", False, plan.get("strategy_runtime_migration")),
        _check("automatic_stitching_false", False, plan.get("automatic_stitching")),
        _check("paper_trading_not_authorized", NOT_AUTHORIZED, plan.get("paper_trading")),
        _check("broker_execution_not_authorized", NOT_AUTHORIZED, plan.get("broker_execution")),
        _check("predictive_usefulness_not_accepted", acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED, plan.get("predictive_usefulness"), severity=INFO),
        _check("profitability_not_accepted", acquisition.PROFITABILITY_NOT_ACCEPTED, plan.get("profitability"), severity=INFO),
        _check("runtime_touchpoint_inventory_present", True, bool(plan.get("runtime_touchpoint_inventory"))),
        _check("future_gates_defined", FUTURE_GATES, plan.get("future_gates")),
        _check("hard_guardrails_defined", HARD_GUARDRAILS, plan.get("hard_guardrails")),
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
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def _digest_payload(plan: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(plan)
    payload.pop("runtime_migration_plan_candidate_digest", None)
    return payload


def runtime_migration_plan_candidate_digest_v1(plan: dict[str, Any]) -> str:
    """Return the deterministic semantic digest for a runtime migration plan candidate."""
    return semantic_digest(_digest_payload(plan))


def build_runtime_migration_plan_candidate_v1() -> dict[str, Any]:
    """Build an offline runtime migration planning artifact without authorizing runtime use."""
    plan: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND_RUNTIME_MIGRATION_PLAN_CANDIDATE,
        "schema_version": SCHEMA_VERSION_RUNTIME_MIGRATION_PLAN_CANDIDATE_V1,
        "plan_status": RUNTIME_MIGRATION_PLAN_READY_FOR_OPERATOR_REVIEW,
        "created_offline": True,
        "provider_requests_made": False,
        "runtime_migration_approved": False,
        "runtime_migration_active": False,
        "strategy_runtime_migration": False,
        "automatic_stitching": False,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "operator_review_required": True,
        "operator_approval_required_before_runtime_use": True,
        "migration_scope": "READ_ONLY_RESEARCH_DATASET_DISCOVERY",
        "runtime_activation_scope": "NONE",
        "strategy_input_replacement": NOT_AUTHORIZED,
        "default_dataset_switch": NOT_AUTHORIZED,
        "paper_trading_scope": NOT_AUTHORIZED,
        "broker_execution_scope": NOT_AUTHORIZED,
        "runtime_readiness_established": False,
        "runtime_touchpoint_inventory_complete": False,
        "planned_phases": list(PLANNED_PHASES),
        "future_gates": list(FUTURE_GATES),
        "hard_guardrails": list(HARD_GUARDRAILS),
        "runtime_touchpoint_inventory": _runtime_touchpoint_inventory(),
        "remaining_roadmap": list(REMAINING_ROADMAP),
        "source_swing_registry_approval_artifact_kind": swing_approval.ARTIFACT_KIND_SWING_REGISTRY_APPROVED,
        "source_position_swing_registry_approval_artifact_kind": (
            position_approval.ARTIFACT_KIND_POSITION_SWING_REGISTRY_APPROVED
        ),
        **_registry_inputs(),
        **_authority_digests(),
    }
    checklist = _build_checklist(plan)
    plan["candidate_checklist"] = checklist
    plan["candidate_summary"] = _summary(checklist)
    plan["runtime_migration_plan_candidate_digest"] = runtime_migration_plan_candidate_digest_v1(plan)
    validate_runtime_migration_plan_candidate_v1(plan)
    return plan


def validate_runtime_migration_plan_candidate_v1(plan: dict[str, Any]) -> dict[str, Any]:
    """Validate a runtime migration planning candidate without approving runtime migration."""
    if not isinstance(plan, dict):
        raise RuntimeMigrationPlanningError("runtime migration plan must be a JSON object")
    _expect(plan.get("artifact_kind"), ARTIFACT_KIND_RUNTIME_MIGRATION_PLAN_CANDIDATE, "artifact_kind")
    _expect(plan.get("schema_version"), SCHEMA_VERSION_RUNTIME_MIGRATION_PLAN_CANDIDATE_V1, "schema_version")
    _expect(plan.get("plan_status"), RUNTIME_MIGRATION_PLAN_READY_FOR_OPERATOR_REVIEW, "plan_status")
    for field in (
        "created_offline",
        "operator_review_required",
        "operator_approval_required_before_runtime_use",
        "swing_registry_approved",
        "position_swing_registry_approved",
    ):
        _expect_true(plan.get(field), field)
    for field in (
        "provider_requests_made",
        "runtime_migration_approved",
        "runtime_migration_active",
        "strategy_runtime_migration",
        "automatic_stitching",
        "runtime_readiness_established",
    ):
        _expect_false(plan.get(field), field)
    _expect(plan.get("runtime_touchpoint_inventory_complete"), False, "runtime_touchpoint_inventory_complete")
    for field in (
        "runtime_use",
        "strategy_use",
        "paper_trading",
        "broker_execution",
        "strategy_input_replacement",
        "default_dataset_switch",
        "paper_trading_scope",
        "broker_execution_scope",
        "swing_runtime_use",
        "position_swing_runtime_use",
        "swing_strategy_use",
        "position_swing_strategy_use",
    ):
        _expect(plan.get(field), NOT_AUTHORIZED, field)
    _expect(plan.get("predictive_usefulness"), acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED, "predictive_usefulness")
    _expect(plan.get("profitability"), acquisition.PROFITABILITY_NOT_ACCEPTED, "profitability")
    for field, expected in {
        "migration_scope": "READ_ONLY_RESEARCH_DATASET_DISCOVERY",
        "runtime_activation_scope": "NONE",
        "source_swing_registry_approval_artifact_kind": swing_approval.ARTIFACT_KIND_SWING_REGISTRY_APPROVED,
        "source_position_swing_registry_approval_artifact_kind": (
            position_approval.ARTIFACT_KIND_POSITION_SWING_REGISTRY_APPROVED
        ),
        "swing_registry_approval_digest": EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST,
        "swing_registry_key": swing_registry.PROPOSED_REGISTRY_KEY,
        "swing_registry_scope": swing_registry.PROPOSED_REGISTRY_SCOPE,
        "swing_dataset_rows_digest": swing_registry.EXPECTED_DATASET_ROWS_DIGEST,
        "swing_dataset_manifest_digest": swing_registry.EXPECTED_DATASET_MANIFEST_DIGEST,
        "swing_bar_count": swing_registry.EXPECTED_SWING_BAR_COUNT,
        "position_swing_registry_approval_digest": EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST,
        "position_swing_registry_key": position_registry.PROPOSED_REGISTRY_KEY,
        "position_swing_registry_scope": position_registry.PROPOSED_REGISTRY_SCOPE,
        "position_swing_dataset_rows_digest": position_registry.EXPECTED_DATASET_ROWS_DIGEST,
        "position_swing_dataset_manifest_digest": position_registry.EXPECTED_DATASET_MANIFEST_DIGEST,
        "position_swing_bar_count": position_registry.EXPECTED_POSITION_SWING_BAR_COUNT,
        **_authority_digests(),
    }.items():
        _expect(plan.get(field), expected, field)
    _expect(plan.get("planned_phases"), PLANNED_PHASES, "planned_phases")
    _expect(plan.get("future_gates"), FUTURE_GATES, "future_gates")
    _expect(plan.get("hard_guardrails"), HARD_GUARDRAILS, "hard_guardrails")
    inventory = plan.get("runtime_touchpoint_inventory")
    if not isinstance(inventory, list) or not inventory:
        raise RuntimeMigrationPlanningError("runtime_touchpoint_inventory missing")
    _expect(plan.get("remaining_roadmap"), REMAINING_ROADMAP, "remaining_roadmap")
    checklist = plan.get("candidate_checklist")
    if not isinstance(checklist, list):
        raise RuntimeMigrationPlanningError("candidate_checklist must be a list")
    _expect([item.get("check_id") for item in checklist if isinstance(item, dict)], REQUIRED_CHECK_IDS, "candidate_checklist check IDs")
    expected_checklist = _build_checklist(plan)
    failed = [item for item in expected_checklist if item["status"] != PASS]
    if failed:
        raise RuntimeMigrationPlanningError(f"candidate checklist contains failed check: {failed[0]['check_id']}")
    _expect(checklist, expected_checklist, "candidate_checklist")
    summary = _summary(checklist)
    _expect(plan.get("candidate_summary"), summary, "candidate_summary")
    _expect_true(summary.get("ready_for_operator_review"), "ready_for_operator_review")
    _expect_false(summary.get("runtime_migration_authorized"), "runtime_migration_authorized")
    _expect_false(summary.get("software_runtime_activation_authorized"), "software_runtime_activation_authorized")
    digest = plan.get("runtime_migration_plan_candidate_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise RuntimeMigrationPlanningError("runtime_migration_plan_candidate_digest missing")
    _expect(digest, runtime_migration_plan_candidate_digest_v1(plan), "runtime_migration_plan_candidate_digest")
    return {
        "status": "RUNTIME_MIGRATION_PLAN_CANDIDATE_VALID",
        "artifact_kind": plan["artifact_kind"],
        "plan_status": plan["plan_status"],
        "runtime_migration_plan_candidate_digest": digest,
        "swing_registry_approval_digest": EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST,
        "position_swing_registry_approval_digest": EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST,
        "runtime_migration_approved": False,
        "runtime_migration_active": False,
        "strategy_runtime_migration": False,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "runtime_touchpoint_inventory_count": len(inventory),
        "runtime_touchpoint_inventory_complete": False,
        "total_checks": summary["total_checks"],
        "passed_checks": summary["passed_checks"],
        "failed_checks": summary["failed_checks"],
        "blocker_count": summary["blocker_count"],
    }


def build_runtime_migration_plan_markdown_v1(plan: dict[str, Any]) -> str:
    """Render a runtime migration planning status document."""
    validation = validate_runtime_migration_plan_candidate_v1(plan)
    summary = plan["candidate_summary"]
    lines = [
        "# MarketFlow Runtime Migration Plan Status",
        "",
        "## Title",
        "- Runtime Migration Planning v1.",
        "",
        "## Purpose",
        "- Define a read-only planning path after SWING and POSITION_SWING research registry approval.",
        "- Preserve all runtime, trading, predictive, and profitability guardrails.",
        "",
        "## Research Registry Inputs",
        f"- SWING registry approval digest: `{plan['swing_registry_approval_digest']}`",
        f"- SWING registry key: `{plan['swing_registry_key']}`",
        f"- POSITION_SWING registry approval digest: `{plan['position_swing_registry_approval_digest']}`",
        f"- POSITION_SWING registry key: `{plan['position_swing_registry_key']}`",
        "",
        "## Runtime Boundary",
        f"- Runtime migration approved: `{plan['runtime_migration_approved']}`",
        f"- Runtime migration active: `{plan['runtime_migration_active']}`",
        f"- Strategy runtime migration: `{plan['strategy_runtime_migration']}`",
        f"- Runtime use: `{plan['runtime_use']}`",
        f"- Strategy use: `{plan['strategy_use']}`",
        f"- Paper trading: `{plan['paper_trading']}`",
        f"- Broker execution: `{plan['broker_execution']}`",
        f"- Predictive usefulness: `{plan['predictive_usefulness']}`",
        f"- Profitability: `{plan['profitability']}`",
        "",
        "## Planned Migration Phases",
    ]
    lines.extend(f"{index}. {phase}" for index, phase in enumerate(plan["planned_phases"], start=1))
    lines.extend(["", "## Future Approval Gates"])
    lines.extend(f"- `{gate}`" for gate in plan["future_gates"])
    lines.extend(["", "## Runtime Touchpoint Inventory"])
    for item in plan["runtime_touchpoint_inventory"]:
        lines.append(
            f"- `{item['path']}`: {item['role']}; risk `{item['risk_level']}`; action: {item['recommended_action']}"
        )
    lines.extend(["", "## Hard Guardrails"])
    lines.extend(f"- {guardrail}" for guardrail in plan["hard_guardrails"])
    lines.extend(
        [
            "",
            "## Checklist Summary",
            f"- Total checks: `{summary['total_checks']}`",
            f"- Passed checks: `{summary['passed_checks']}`",
            f"- Failed checks: `{summary['failed_checks']}`",
            f"- Blocker count: `{summary['blocker_count']}`",
            f"- Runtime migration authorized: `{summary['runtime_migration_authorized']}`",
            f"- Software runtime activation authorized: `{summary['software_runtime_activation_authorized']}`",
            "",
            "## Remaining Roadmap",
        ]
    )
    lines.extend(f"{index}. {task}" for index, task in enumerate(plan["remaining_roadmap"], start=1))
    lines.extend(
        [
            "",
            "## Non-Goals",
            "- No Massive.com / Polygon provider data was fetched.",
            "- No acquisition rows, SWING bars, or POSITION_SWING bars were regenerated.",
            "- No Strategy runtime migration was approved or activated.",
            "- Runtime, Strategy, paper trading, and broker execution use remain `NOT_AUTHORIZED`.",
            "- Predictive usefulness and profitability remain not accepted.",
            "",
            "## Plan Digest",
            f"- Runtime migration plan candidate digest: `{validation['runtime_migration_plan_candidate_digest']}`",
            "",
        ]
    )
    return "\n".join(lines)


def write_runtime_migration_plan_candidate_v1(
    output_dir: str | Path,
    *,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write the runtime migration plan candidate JSON artifact without overwriting output."""
    plan = build_runtime_migration_plan_candidate_v1()
    validation = validate_runtime_migration_plan_candidate_v1(plan)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "runtime_migration_plan_candidate_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise RuntimeMigrationPlanningError("runtime migration plan filename must be a simple JSON filename")
    path = directory / output_name
    if path.exists():
        raise RuntimeMigrationPlanningError("runtime migration plan output already exists")
    payload = canonical_json_bytes(plan)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": str(path),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
    }
