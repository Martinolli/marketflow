"""Offline operator-review package for runtime migration plan candidates."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import runtime_migration_planning_service as planning


ARTIFACT_KIND_RUNTIME_MIGRATION_PLAN_CANDIDATE_REVIEW_PACKAGE = (
    "RUNTIME_MIGRATION_PLAN_CANDIDATE_REVIEW_PACKAGE"
)
SCHEMA_VERSION_RUNTIME_MIGRATION_PLAN_CANDIDATE_REVIEW_V1 = "runtime_migration_plan_candidate_review_v1"
RUNTIME_MIGRATION_PLAN_CANDIDATE_REVIEW_PACKAGE_READY = (
    "RUNTIME_MIGRATION_PLAN_CANDIDATE_REVIEW_PACKAGE_READY"
)
RUNTIME_MIGRATION_PLAN_STATUS_BINDING = "RUNTIME_MIGRATION_PLAN_STATUS_BINDING"
RUNTIME_MIGRATION_PLAN_OBJECT_BINDING = "RUNTIME_MIGRATION_PLAN_OBJECT_BINDING"
RUNTIME_TOUCHPOINT_INVENTORY_INCOMPLETE_COMPACT = "INCOMPLETE_COMPACT"

EXPECTED_RUNTIME_MIGRATION_PLAN_DIGEST = "f1b7b1456b69774c6e19fa81cf11a319ff5b9c2a9cc75410b7873ed9417e68a5"
EXPECTED_PLAN_CHECKLIST_TOTAL = len(planning.REQUIRED_CHECK_IDS)
EXPECTED_PLAN_CHECKLIST_PASSED = len(planning.REQUIRED_CHECK_IDS)
EXPECTED_PLAN_CHECKLIST_FAILED = 0
EXPECTED_PLAN_BLOCKER_COUNT = 0

PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
INFO = "INFO"

REQUIRED_CHECK_IDS = [
    "runtime_plan_kind_matches",
    "runtime_plan_status_ready_for_review",
    "runtime_plan_digest_matches",
    "runtime_plan_checklist_zero_blockers",
    "swing_registry_approval_digest_bound",
    "position_swing_registry_approval_digest_bound",
    "swing_registry_scope_research_dataset",
    "position_swing_registry_scope_research_dataset",
    "swing_runtime_use_not_authorized",
    "position_swing_runtime_use_not_authorized",
    "swing_strategy_use_not_authorized",
    "position_swing_strategy_use_not_authorized",
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
    "planned_phases_confirmed",
    "future_gates_confirmed",
    "hard_guardrails_confirmed",
    "runtime_touchpoint_inventory_present",
    "runtime_touchpoint_inventory_incomplete_compact_acknowledged",
    "provider_requests_made_in_review_false",
    "no_runtime_migration_approved_artifact_created",
]

REMAINING_REQUIRED_TASKS = [
    "Read-only registry discovery candidate.",
    "Dataset file availability verification.",
    "Research-only applicability campaign plan.",
    "Research-only applicability campaign execution.",
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


class RuntimeMigrationOperatorReviewError(ValueError):
    """Raised when a runtime migration review package violates guardrails."""


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
        raise RuntimeMigrationOperatorReviewError(f"{field_name} mismatch")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise RuntimeMigrationOperatorReviewError(f"{field_name} must be false")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise RuntimeMigrationOperatorReviewError(f"{field_name} must be true")


def _review_context() -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_RUNTIME_MIGRATION_PLAN_CANDIDATE_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_RUNTIME_MIGRATION_PLAN_CANDIDATE_REVIEW_V1,
        "review_status": RUNTIME_MIGRATION_PLAN_CANDIDATE_REVIEW_PACKAGE_READY,
        "operator_decision_required": True,
        "operator_decision": None,
        "operator_approved_by": None,
        "operator_approval_timestamp": None,
        "operator_approval_digest": None,
        "operator_signature": None,
        "approval_status": None,
        "runtime_migration_approved": False,
        "runtime_migration_active": False,
        "strategy_runtime_migration": False,
        "runtime_use": planning.NOT_AUTHORIZED,
        "strategy_use": planning.NOT_AUTHORIZED,
        "paper_trading": planning.NOT_AUTHORIZED,
        "broker_execution": planning.NOT_AUTHORIZED,
        "automatic_stitching": False,
        "created_offline": True,
        "provider_requests_made_in_review": False,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "software_runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def _plan_evidence_from_candidate(plan_candidate: dict[str, Any]) -> dict[str, Any]:
    try:
        validation = planning.validate_runtime_migration_plan_candidate_v1(plan_candidate)
    except planning.RuntimeMigrationPlanningError as exc:
        raise RuntimeMigrationOperatorReviewError(f"source runtime migration plan candidate invalid: {exc}") from exc
    inventory = plan_candidate["runtime_touchpoint_inventory"]
    inventory_status = (
        RUNTIME_TOUCHPOINT_INVENTORY_INCOMPLETE_COMPACT
        if plan_candidate.get("runtime_touchpoint_inventory_complete") is False
        else "COMPLETE"
    )
    return {
        "reviewed_plan_kind": plan_candidate["artifact_kind"],
        "reviewed_plan_status": plan_candidate["plan_status"],
        "reviewed_plan_digest": validation["runtime_migration_plan_candidate_digest"],
        "reviewed_plan_checklist_total": validation["total_checks"],
        "reviewed_plan_checklist_passed": validation["passed_checks"],
        "reviewed_plan_checklist_failed": validation["failed_checks"],
        "reviewed_plan_blocker_count": validation["blocker_count"],
        "runtime_touchpoint_inventory_count": validation["runtime_touchpoint_inventory_count"],
        "runtime_touchpoint_inventory_status": inventory_status,
        "runtime_touchpoint_inventory": deepcopy(inventory),
        "planned_phases": list(plan_candidate["planned_phases"]),
        "future_gates": list(plan_candidate["future_gates"]),
        "hard_guardrails": list(plan_candidate["hard_guardrails"]),
        "migration_scope": plan_candidate["migration_scope"],
        "runtime_activation_scope": plan_candidate["runtime_activation_scope"],
        "strategy_input_replacement": plan_candidate["strategy_input_replacement"],
        "default_dataset_switch": plan_candidate["default_dataset_switch"],
        "paper_trading_scope": plan_candidate["paper_trading_scope"],
        "broker_execution_scope": plan_candidate["broker_execution_scope"],
        "swing_registry_approved": plan_candidate["swing_registry_approved"],
        "swing_registry_approval_digest": plan_candidate["swing_registry_approval_digest"],
        "swing_registry_key": plan_candidate["swing_registry_key"],
        "swing_registry_scope": plan_candidate["swing_registry_scope"],
        "swing_runtime_use": plan_candidate["swing_runtime_use"],
        "swing_strategy_use": plan_candidate["swing_strategy_use"],
        "swing_dataset_rows_digest": plan_candidate["swing_dataset_rows_digest"],
        "swing_dataset_manifest_digest": plan_candidate["swing_dataset_manifest_digest"],
        "swing_bar_count": plan_candidate["swing_bar_count"],
        "position_swing_registry_approved": plan_candidate["position_swing_registry_approved"],
        "position_swing_registry_approval_digest": plan_candidate["position_swing_registry_approval_digest"],
        "position_swing_registry_key": plan_candidate["position_swing_registry_key"],
        "position_swing_registry_scope": plan_candidate["position_swing_registry_scope"],
        "position_swing_runtime_use": plan_candidate["position_swing_runtime_use"],
        "position_swing_strategy_use": plan_candidate["position_swing_strategy_use"],
        "position_swing_dataset_rows_digest": plan_candidate["position_swing_dataset_rows_digest"],
        "position_swing_dataset_manifest_digest": plan_candidate["position_swing_dataset_manifest_digest"],
        "position_swing_bar_count": plan_candidate["position_swing_bar_count"],
        "identity_frozen_digest": plan_candidate["identity_frozen_digest"],
        "calendar_frozen_digest": plan_candidate["calendar_frozen_digest"],
        "schedule_digest": plan_candidate["schedule_digest"],
        "split_event_frozen_digest": plan_candidate["split_event_frozen_digest"],
        "dividend_event_frozen_digest": plan_candidate["dividend_event_frozen_digest"],
        "acquisition_generation_frozen_digest": plan_candidate["acquisition_generation_frozen_digest"],
    }


def _recorded_plan_evidence() -> dict[str, Any]:
    return _plan_evidence_from_candidate(planning.build_runtime_migration_plan_candidate_v1())


def _build_checklist(review_package: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        _check("runtime_plan_kind_matches", planning.ARTIFACT_KIND_RUNTIME_MIGRATION_PLAN_CANDIDATE, review_package.get("reviewed_plan_kind")),
        _check("runtime_plan_status_ready_for_review", planning.RUNTIME_MIGRATION_PLAN_READY_FOR_OPERATOR_REVIEW, review_package.get("reviewed_plan_status")),
        _check("runtime_plan_digest_matches", EXPECTED_RUNTIME_MIGRATION_PLAN_DIGEST, review_package.get("reviewed_plan_digest")),
        _check(
            "runtime_plan_checklist_zero_blockers",
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
        _check("swing_registry_approval_digest_bound", planning.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST, review_package.get("swing_registry_approval_digest")),
        _check("position_swing_registry_approval_digest_bound", planning.EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST, review_package.get("position_swing_registry_approval_digest")),
        _check("swing_registry_scope_research_dataset", "RESEARCH_DATASET", review_package.get("swing_registry_scope")),
        _check("position_swing_registry_scope_research_dataset", "RESEARCH_DATASET", review_package.get("position_swing_registry_scope")),
        _check("swing_runtime_use_not_authorized", planning.NOT_AUTHORIZED, review_package.get("swing_runtime_use")),
        _check("position_swing_runtime_use_not_authorized", planning.NOT_AUTHORIZED, review_package.get("position_swing_runtime_use")),
        _check("swing_strategy_use_not_authorized", planning.NOT_AUTHORIZED, review_package.get("swing_strategy_use")),
        _check("position_swing_strategy_use_not_authorized", planning.NOT_AUTHORIZED, review_package.get("position_swing_strategy_use")),
        _check("runtime_migration_approved_false", False, review_package.get("runtime_migration_approved")),
        _check("runtime_migration_active_false", False, review_package.get("runtime_migration_active")),
        _check("strategy_runtime_migration_false", False, review_package.get("strategy_runtime_migration")),
        _check("runtime_use_not_authorized", planning.NOT_AUTHORIZED, review_package.get("runtime_use")),
        _check("strategy_use_not_authorized", planning.NOT_AUTHORIZED, review_package.get("strategy_use")),
        _check("paper_trading_not_authorized", planning.NOT_AUTHORIZED, review_package.get("paper_trading")),
        _check("broker_execution_not_authorized", planning.NOT_AUTHORIZED, review_package.get("broker_execution")),
        _check("automatic_stitching_false", False, review_package.get("automatic_stitching")),
        _check("predictive_usefulness_not_accepted", acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED, review_package.get("predictive_usefulness"), severity=INFO),
        _check("profitability_not_accepted", acquisition.PROFITABILITY_NOT_ACCEPTED, review_package.get("profitability"), severity=INFO),
        _check("planned_phases_confirmed", planning.PLANNED_PHASES, review_package.get("planned_phases")),
        _check("future_gates_confirmed", planning.FUTURE_GATES, review_package.get("future_gates")),
        _check("hard_guardrails_confirmed", planning.HARD_GUARDRAILS, review_package.get("hard_guardrails")),
        _check("runtime_touchpoint_inventory_present", True, bool(review_package.get("runtime_touchpoint_inventory"))),
        _check(
            "runtime_touchpoint_inventory_incomplete_compact_acknowledged",
            {
                "count": 10,
                "status": RUNTIME_TOUCHPOINT_INVENTORY_INCOMPLETE_COMPACT,
            },
            {
                "count": review_package.get("runtime_touchpoint_inventory_count"),
                "status": review_package.get("runtime_touchpoint_inventory_status"),
            },
        ),
        _check("provider_requests_made_in_review_false", False, review_package.get("provider_requests_made_in_review")),
        _check(
            "no_runtime_migration_approved_artifact_created",
            {
                "artifact_kind_is_not_runtime_migration_approved": True,
                "review_status_is_not_runtime_migration_approved": True,
                "approval_status_is_null": True,
                "runtime_migration_approved_is_false": True,
                "runtime_migration_active_is_false": True,
            },
            {
                "artifact_kind_is_not_runtime_migration_approved": (
                    review_package.get("artifact_kind") != "RUNTIME_MIGRATION_APPROVED"
                ),
                "review_status_is_not_runtime_migration_approved": (
                    review_package.get("review_status") != "RUNTIME_MIGRATION_APPROVED"
                ),
                "approval_status_is_null": review_package.get("approval_status") is None,
                "runtime_migration_approved_is_false": review_package.get("runtime_migration_approved") is False,
                "runtime_migration_active_is_false": review_package.get("runtime_migration_active") is False,
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
        "operator_decision_required_before_runtime_migration": True,
        "software_runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def _digest_payload(review_package: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(review_package)
    payload.pop("runtime_migration_review_package_digest", None)
    return payload


def runtime_migration_review_package_digest_v1(review_package: dict[str, Any]) -> str:
    """Return the deterministic semantic digest for a runtime migration review package."""
    return semantic_digest(_digest_payload(review_package))


def build_runtime_migration_plan_candidate_review_package_v1(
    plan_candidate: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build an offline review package for a runtime migration plan candidate."""
    binding_mode = RUNTIME_MIGRATION_PLAN_STATUS_BINDING
    evidence = _recorded_plan_evidence()
    if plan_candidate is not None:
        binding_mode = RUNTIME_MIGRATION_PLAN_OBJECT_BINDING
        evidence = _plan_evidence_from_candidate(plan_candidate)
    review_package = {
        **_review_context(),
        "binding_mode": binding_mode,
        **evidence,
        "remaining_required_tasks": list(REMAINING_REQUIRED_TASKS),
    }
    checklist = _build_checklist(review_package)
    review_package["review_checklist"] = checklist
    review_package["review_summary"] = _summary(checklist)
    review_package["runtime_migration_review_package_digest"] = runtime_migration_review_package_digest_v1(
        review_package
    )
    validate_runtime_migration_plan_candidate_review_package_v1(review_package)
    return review_package


def _reject_forbidden_values(mapping: dict[str, Any], *, path: str = "review_package") -> None:
    for key, value in mapping.items():
        current_path = f"{path}.{key}"
        if isinstance(value, str) and value in {
            "RUNTIME_MIGRATION_APPROVED",
            "RUNTIME_MIGRATION_ACTIVE",
            "STRATEGY_RUNTIME_MIGRATION",
        }:
            raise RuntimeMigrationOperatorReviewError(f"{current_path} must not emit {value}")
        if key in FORBIDDEN_APPROVAL_FIELDS and value is not None:
            raise RuntimeMigrationOperatorReviewError(f"{current_path} must be null")
        if key in {"runtime_migration_approved", "runtime_migration_active", "strategy_runtime_migration", "automatic_stitching"}:
            if value is True:
                raise RuntimeMigrationOperatorReviewError(f"{current_path} must be false")
        if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution", "swing_runtime_use", "position_swing_runtime_use", "swing_strategy_use", "position_swing_strategy_use"}:
            if value == "AUTHORIZED":
                raise RuntimeMigrationOperatorReviewError(f"{current_path} must not be AUTHORIZED")
        if key in {"predictive_usefulness", "profitability"} and value == "accepted":
            raise RuntimeMigrationOperatorReviewError(f"{current_path} must not be accepted")
        if isinstance(value, dict):
            _reject_forbidden_values(value, path=current_path)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, dict):
                    _reject_forbidden_values(item, path=f"{current_path}[{index}]")


def validate_runtime_migration_plan_candidate_review_package_v1(
    review_package: dict[str, Any],
) -> dict[str, Any]:
    """Validate a runtime migration review package without granting runtime authority."""
    if not isinstance(review_package, dict):
        raise RuntimeMigrationOperatorReviewError("runtime migration review package must be a JSON object")
    _reject_forbidden_values(review_package)
    _expect(
        review_package.get("artifact_kind"),
        ARTIFACT_KIND_RUNTIME_MIGRATION_PLAN_CANDIDATE_REVIEW_PACKAGE,
        "artifact_kind",
    )
    _expect(
        review_package.get("schema_version"),
        SCHEMA_VERSION_RUNTIME_MIGRATION_PLAN_CANDIDATE_REVIEW_V1,
        "schema_version",
    )
    _expect(
        review_package.get("review_status"),
        RUNTIME_MIGRATION_PLAN_CANDIDATE_REVIEW_PACKAGE_READY,
        "review_status",
    )
    if review_package.get("binding_mode") not in {
        RUNTIME_MIGRATION_PLAN_STATUS_BINDING,
        RUNTIME_MIGRATION_PLAN_OBJECT_BINDING,
    }:
        raise RuntimeMigrationOperatorReviewError("binding_mode mismatch")
    _expect_true(review_package.get("operator_decision_required"), "operator_decision_required")
    _expect(review_package.get("operator_decision"), None, "operator_decision")
    _expect_true(review_package.get("created_offline"), "created_offline")
    for field in FORBIDDEN_APPROVAL_FIELDS:
        _expect(review_package.get(field), None, field)
    for field in (
        "runtime_migration_approved",
        "runtime_migration_active",
        "strategy_runtime_migration",
        "automatic_stitching",
        "provider_requests_made_in_review",
        "software_runtime_migration_authorized",
        "software_runtime_activation_authorized",
    ):
        _expect_false(review_package.get(field), field)
    for field in (
        "runtime_use",
        "strategy_use",
        "paper_trading",
        "broker_execution",
        "swing_runtime_use",
        "position_swing_runtime_use",
        "swing_strategy_use",
        "position_swing_strategy_use",
        "strategy_input_replacement",
        "default_dataset_switch",
        "paper_trading_scope",
        "broker_execution_scope",
    ):
        _expect(review_package.get(field), planning.NOT_AUTHORIZED, field)
    _expect(
        review_package.get("predictive_usefulness"),
        acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "predictive_usefulness",
    )
    _expect(review_package.get("profitability"), acquisition.PROFITABILITY_NOT_ACCEPTED, "profitability")
    for field, expected in {
        "reviewed_plan_kind": planning.ARTIFACT_KIND_RUNTIME_MIGRATION_PLAN_CANDIDATE,
        "reviewed_plan_status": planning.RUNTIME_MIGRATION_PLAN_READY_FOR_OPERATOR_REVIEW,
        "reviewed_plan_digest": EXPECTED_RUNTIME_MIGRATION_PLAN_DIGEST,
        "reviewed_plan_checklist_total": EXPECTED_PLAN_CHECKLIST_TOTAL,
        "reviewed_plan_checklist_passed": EXPECTED_PLAN_CHECKLIST_PASSED,
        "reviewed_plan_checklist_failed": EXPECTED_PLAN_CHECKLIST_FAILED,
        "reviewed_plan_blocker_count": EXPECTED_PLAN_BLOCKER_COUNT,
        "runtime_touchpoint_inventory_count": 10,
        "runtime_touchpoint_inventory_status": RUNTIME_TOUCHPOINT_INVENTORY_INCOMPLETE_COMPACT,
        "migration_scope": "READ_ONLY_RESEARCH_DATASET_DISCOVERY",
        "runtime_activation_scope": "NONE",
        "swing_registry_approved": True,
        "swing_registry_approval_digest": planning.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST,
        "swing_registry_key": planning.swing_registry.PROPOSED_REGISTRY_KEY,
        "swing_registry_scope": planning.swing_registry.PROPOSED_REGISTRY_SCOPE,
        "swing_dataset_rows_digest": planning.swing_registry.EXPECTED_DATASET_ROWS_DIGEST,
        "swing_dataset_manifest_digest": planning.swing_registry.EXPECTED_DATASET_MANIFEST_DIGEST,
        "swing_bar_count": planning.swing_registry.EXPECTED_SWING_BAR_COUNT,
        "position_swing_registry_approved": True,
        "position_swing_registry_approval_digest": planning.EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST,
        "position_swing_registry_key": planning.position_registry.PROPOSED_REGISTRY_KEY,
        "position_swing_registry_scope": planning.position_registry.PROPOSED_REGISTRY_SCOPE,
        "position_swing_dataset_rows_digest": planning.position_registry.EXPECTED_DATASET_ROWS_DIGEST,
        "position_swing_dataset_manifest_digest": planning.position_registry.EXPECTED_DATASET_MANIFEST_DIGEST,
        "position_swing_bar_count": planning.position_registry.EXPECTED_POSITION_SWING_BAR_COUNT,
        **planning._authority_digests(),
    }.items():
        _expect(review_package.get(field), expected, field)
    _expect(review_package.get("planned_phases"), planning.PLANNED_PHASES, "planned_phases")
    _expect(review_package.get("future_gates"), planning.FUTURE_GATES, "future_gates")
    _expect(review_package.get("hard_guardrails"), planning.HARD_GUARDRAILS, "hard_guardrails")
    inventory = review_package.get("runtime_touchpoint_inventory")
    if not isinstance(inventory, list) or len(inventory) != 10:
        raise RuntimeMigrationOperatorReviewError("runtime_touchpoint_inventory missing")
    _expect(review_package.get("remaining_required_tasks"), REMAINING_REQUIRED_TASKS, "remaining_required_tasks")
    checklist = review_package.get("review_checklist")
    if not isinstance(checklist, list):
        raise RuntimeMigrationOperatorReviewError("review_checklist must be a list")
    _expect(
        [item.get("check_id") for item in checklist if isinstance(item, dict)],
        REQUIRED_CHECK_IDS,
        "review_checklist check IDs",
    )
    expected_checklist = _build_checklist(review_package)
    failed = [item for item in expected_checklist if item["status"] != PASS]
    if failed:
        raise RuntimeMigrationOperatorReviewError(
            f"runtime migration review checklist contains failed check: {failed[0]['check_id']}"
        )
    _expect(checklist, expected_checklist, "review_checklist")
    summary = _summary(checklist)
    _expect(review_package.get("review_summary"), summary, "review_summary")
    _expect_true(summary.get("ready_for_operator_assessment"), "ready_for_operator_assessment")
    _expect_true(
        summary.get("operator_decision_required_before_runtime_migration"),
        "operator_decision_required_before_runtime_migration",
    )
    _expect_false(summary.get("software_runtime_migration_authorized"), "software_runtime_migration_authorized")
    _expect_false(summary.get("software_runtime_activation_authorized"), "software_runtime_activation_authorized")
    digest = review_package.get("runtime_migration_review_package_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise RuntimeMigrationOperatorReviewError("runtime_migration_review_package_digest missing")
    _expect(digest, runtime_migration_review_package_digest_v1(review_package), "runtime_migration_review_package_digest")
    return {
        "status": "RUNTIME_MIGRATION_PLAN_CANDIDATE_REVIEW_PACKAGE_VALID",
        "artifact_kind": review_package["artifact_kind"],
        "review_status": review_package["review_status"],
        "runtime_migration_review_package_digest": digest,
        "reviewed_plan_digest": EXPECTED_RUNTIME_MIGRATION_PLAN_DIGEST,
        "swing_registry_approval_digest": planning.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST,
        "position_swing_registry_approval_digest": planning.EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST,
        "runtime_migration_approved": False,
        "runtime_migration_active": False,
        "strategy_runtime_migration": False,
        "runtime_use": planning.NOT_AUTHORIZED,
        "strategy_use": planning.NOT_AUTHORIZED,
        "paper_trading": planning.NOT_AUTHORIZED,
        "broker_execution": planning.NOT_AUTHORIZED,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "runtime_touchpoint_inventory_count": 10,
        "runtime_touchpoint_inventory_status": RUNTIME_TOUCHPOINT_INVENTORY_INCOMPLETE_COMPACT,
        "total_checks": summary["total_checks"],
        "passed_checks": summary["passed_checks"],
        "failed_checks": summary["failed_checks"],
        "blocker_count": summary["blocker_count"],
    }


def build_runtime_migration_plan_candidate_review_markdown_v1(review_package: dict[str, Any]) -> str:
    """Render a runtime migration review package status document."""
    validation = validate_runtime_migration_plan_candidate_review_package_v1(review_package)
    summary = review_package["review_summary"]
    lines = [
        "# MarketFlow Runtime Migration Operator Review Package Status",
        "",
        "## Title",
        "- Runtime Migration Operator Review Package v1.",
        "",
        "## Reviewed Runtime Migration Plan",
        f"- Review package artifact kind: `{review_package['artifact_kind']}`",
        f"- Review status: `{review_package['review_status']}`",
        f"- Binding mode: `{review_package['binding_mode']}`",
        f"- Reviewed plan kind: `{review_package['reviewed_plan_kind']}`",
        f"- Reviewed plan status: `{review_package['reviewed_plan_status']}`",
        f"- Reviewed plan digest: `{review_package['reviewed_plan_digest']}`",
        "",
        "## Registry Inputs",
        f"- SWING registry approval digest: `{review_package['swing_registry_approval_digest']}`",
        f"- SWING registry key: `{review_package['swing_registry_key']}`",
        f"- POSITION_SWING registry approval digest: `{review_package['position_swing_registry_approval_digest']}`",
        f"- POSITION_SWING registry key: `{review_package['position_swing_registry_key']}`",
        "",
        "## Runtime Boundary",
        f"- Runtime migration approved: `{review_package['runtime_migration_approved']}`",
        f"- Runtime migration active: `{review_package['runtime_migration_active']}`",
        f"- Strategy runtime migration: `{review_package['strategy_runtime_migration']}`",
        f"- Runtime use: `{review_package['runtime_use']}`",
        f"- Strategy use: `{review_package['strategy_use']}`",
        f"- Paper trading: `{review_package['paper_trading']}`",
        f"- Broker execution: `{review_package['broker_execution']}`",
        f"- Predictive usefulness: `{review_package['predictive_usefulness']}`",
        f"- Profitability: `{review_package['profitability']}`",
        "",
        "## Planned Phases",
    ]
    lines.extend(f"{index}. {phase}" for index, phase in enumerate(review_package["planned_phases"], start=1))
    lines.extend(["", "## Future Gates"])
    lines.extend(f"- `{gate}`" for gate in review_package["future_gates"])
    lines.extend(["", "## Hard Guardrails"])
    lines.extend(f"- {guardrail}" for guardrail in review_package["hard_guardrails"])
    lines.extend(
        [
            "",
            "## Touchpoint Inventory Note",
            f"- Inventory count: `{review_package['runtime_touchpoint_inventory_count']}`",
            f"- Inventory status: `{review_package['runtime_touchpoint_inventory_status']}`",
            "",
            "## Checklist Summary",
            f"- Total checks: `{summary['total_checks']}`",
            f"- Passed checks: `{summary['passed_checks']}`",
            f"- Failed checks: `{summary['failed_checks']}`",
            f"- Blocker count: `{summary['blocker_count']}`",
            f"- Runtime migration authorized: `{summary['software_runtime_migration_authorized']}`",
            f"- Runtime activation authorized: `{summary['software_runtime_activation_authorized']}`",
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
            "- No Massive.com / Polygon provider data was fetched.",
            "- No acquisition rows, SWING bars, or POSITION_SWING bars were regenerated.",
            "- No `RUNTIME_MIGRATION_APPROVED`, `RUNTIME_MIGRATION_ACTIVE`, or `STRATEGY_RUNTIME_MIGRATION` artifact or status is created.",
            "- Runtime, Strategy, paper trading, and broker execution use remain `NOT_AUTHORIZED`.",
            "- Predictive usefulness and profitability remain not accepted.",
            "",
            "## Review Package Digest",
            f"- Review package digest: `{validation['runtime_migration_review_package_digest']}`",
            "",
        ]
    )
    return "\n".join(lines)


def write_runtime_migration_plan_candidate_review_package_v1(
    output_dir: str | Path,
    *,
    plan_candidate: dict[str, Any] | None = None,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write the runtime migration review package JSON artifact without overwriting output."""
    review_package = build_runtime_migration_plan_candidate_review_package_v1(plan_candidate)
    validation = validate_runtime_migration_plan_candidate_review_package_v1(review_package)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "runtime_migration_plan_candidate_review_package_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise RuntimeMigrationOperatorReviewError("runtime migration review package filename must be a simple JSON filename")
    path = directory / output_name
    if path.exists():
        raise RuntimeMigrationOperatorReviewError("runtime migration review package output already exists")
    payload = canonical_json_bytes(review_package)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": str(path),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
    }
