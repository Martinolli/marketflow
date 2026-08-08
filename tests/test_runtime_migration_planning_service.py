from __future__ import annotations

from pathlib import Path

import pytest

from marketflow.services import runtime_migration_planning_service as planning


def _plan() -> dict:
    return planning.build_runtime_migration_plan_candidate_v1()


def test_plan_candidate_builds_offline_without_provider_calls(monkeypatch: pytest.MonkeyPatch):
    def fail_provider_call(*_args, **_kwargs):  # pragma: no cover
        raise AssertionError("provider path must not be called")

    monkeypatch.setattr(planning.acquisition, "fetch_massive_custom_bars_v1", fail_provider_call)

    plan = _plan()

    assert plan["created_offline"] is True
    assert plan["provider_requests_made"] is False


def test_artifact_kind_is_runtime_migration_plan_candidate():
    assert _plan()["artifact_kind"] == planning.ARTIFACT_KIND_RUNTIME_MIGRATION_PLAN_CANDIDATE


def test_plan_status_is_ready_for_operator_review():
    assert _plan()["plan_status"] == planning.RUNTIME_MIGRATION_PLAN_READY_FOR_OPERATOR_REVIEW


def test_swing_registry_approval_digest_is_bound():
    assert _plan()["swing_registry_approval_digest"] == planning.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST


def test_position_swing_registry_approval_digest_is_bound():
    assert (
        _plan()["position_swing_registry_approval_digest"]
        == planning.EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST
    )


def test_registry_keys_match_accepted_values():
    plan = _plan()

    assert plan["swing_registry_key"] == planning.swing_registry.PROPOSED_REGISTRY_KEY
    assert plan["position_swing_registry_key"] == planning.position_registry.PROPOSED_REGISTRY_KEY


def test_registry_scopes_are_research_dataset():
    plan = _plan()

    assert plan["swing_registry_scope"] == "RESEARCH_DATASET"
    assert plan["position_swing_registry_scope"] == "RESEARCH_DATASET"


def test_runtime_use_remains_not_authorized():
    assert _plan()["runtime_use"] == "NOT_AUTHORIZED"


def test_strategy_use_remains_not_authorized():
    assert _plan()["strategy_use"] == "NOT_AUTHORIZED"


def test_paper_trading_remains_not_authorized():
    assert _plan()["paper_trading"] == "NOT_AUTHORIZED"


def test_broker_execution_remains_not_authorized():
    assert _plan()["broker_execution"] == "NOT_AUTHORIZED"


def test_strategy_runtime_migration_remains_false():
    assert _plan()["strategy_runtime_migration"] is False


def test_automatic_stitching_remains_false():
    assert _plan()["automatic_stitching"] is False


def test_predictive_usefulness_remains_not_accepted():
    assert _plan()["predictive_usefulness"] == "not accepted"


def test_profitability_remains_not_accepted():
    assert _plan()["profitability"] == "not accepted"


def test_planned_phases_include_read_only_registry_discovery():
    assert "Read-only registry discovery service." in _plan()["planned_phases"]


def test_future_gates_include_predictive_and_runtime_approval_reviews():
    gates = _plan()["future_gates"]

    assert "predictive_usefulness_review" in gates
    assert "runtime_migration_operator_approval" in gates


def test_hard_guardrails_include_no_runtime_default_change_and_no_broker_execution():
    guardrails = _plan()["hard_guardrails"]

    assert "no runtime default change" in guardrails
    assert "no broker execution" in guardrails


def test_runtime_touchpoint_inventory_is_present():
    plan = _plan()

    assert plan["runtime_touchpoint_inventory"]
    assert plan["runtime_touchpoint_inventory_complete"] is False


def test_checklist_contains_all_required_check_ids():
    assert [item["check_id"] for item in _plan()["candidate_checklist"]] == planning.REQUIRED_CHECK_IDS


def test_all_checks_pass_for_accepted_plan():
    assert {item["status"] for item in _plan()["candidate_checklist"]} == {"PASS"}


def test_summary_counts_total_passed_failed_correctly():
    plan = _plan()
    summary = plan["candidate_summary"]

    assert summary["total_checks"] == len(planning.REQUIRED_CHECK_IDS)
    assert summary["passed_checks"] == len(planning.REQUIRED_CHECK_IDS)
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["ready_for_operator_review"] is True
    assert summary["runtime_migration_authorized"] is False
    assert summary["software_runtime_activation_authorized"] is False


def test_plan_digest_is_deterministic():
    first = _plan()
    second = _plan()

    assert first["runtime_migration_plan_candidate_digest"] == second["runtime_migration_plan_candidate_digest"]
    assert first["runtime_migration_plan_candidate_digest"] == planning.runtime_migration_plan_candidate_digest_v1(first)


def test_validator_accepts_valid_plan():
    validation = planning.validate_runtime_migration_plan_candidate_v1(_plan())

    assert validation["status"] == "RUNTIME_MIGRATION_PLAN_CANDIDATE_VALID"
    assert validation["runtime_migration_approved"] is False
    assert validation["runtime_migration_active"] is False


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("artifact_kind", "WRONG", "artifact_kind"),
        ("runtime_migration_approved", True, "runtime_migration_approved"),
        ("runtime_migration_active", True, "runtime_migration_active"),
        ("strategy_runtime_migration", True, "strategy_runtime_migration"),
        ("automatic_stitching", True, "automatic_stitching"),
        ("runtime_use", "AUTHORIZED", "runtime_use"),
        ("strategy_use", "AUTHORIZED", "strategy_use"),
        ("paper_trading", "AUTHORIZED", "paper_trading"),
        ("broker_execution", "AUTHORIZED", "broker_execution"),
        ("predictive_usefulness", "accepted", "predictive_usefulness"),
        ("profitability", "accepted", "profitability"),
        ("swing_registry_approval_digest", None, "swing_registry_approval_digest"),
        ("position_swing_registry_approval_digest", None, "position_swing_registry_approval_digest"),
        ("swing_registry_key", "AAPL:WRONG", "swing_registry_key"),
        ("position_swing_registry_key", "AAPL:WRONG", "position_swing_registry_key"),
        ("swing_registry_scope", "RUNTIME_DATASET", "swing_registry_scope"),
        ("position_swing_registry_scope", "RUNTIME_DATASET", "position_swing_registry_scope"),
        ("future_gates", [], "future_gates"),
        ("hard_guardrails", [], "hard_guardrails"),
    ],
)
def test_validator_rejects_invalid_mutations(field: str, value, match: str):
    plan = _plan()
    plan[field] = value

    with pytest.raises(planning.RuntimeMigrationPlanningError, match=match):
        planning.validate_runtime_migration_plan_candidate_v1(plan)


def test_validator_rejects_missing_touchpoint_inventory():
    plan = _plan()
    plan["runtime_touchpoint_inventory"] = []

    with pytest.raises(planning.RuntimeMigrationPlanningError, match="runtime_touchpoint_inventory"):
        planning.validate_runtime_migration_plan_candidate_v1(plan)


def test_validator_rejects_missing_plan_digest():
    plan = _plan()
    plan.pop("runtime_migration_plan_candidate_digest")

    with pytest.raises(planning.RuntimeMigrationPlanningError, match="runtime_migration_plan_candidate_digest"):
        planning.validate_runtime_migration_plan_candidate_v1(plan)


def test_markdown_writer_includes_required_sections_and_guardrails():
    markdown = planning.build_runtime_migration_plan_markdown_v1(_plan())

    for section in (
        "## Title",
        "## Purpose",
        "## Research Registry Inputs",
        "## Runtime Boundary",
        "## Planned Migration Phases",
        "## Future Approval Gates",
        "## Runtime Touchpoint Inventory",
        "## Hard Guardrails",
        "## Checklist Summary",
        "## Remaining Roadmap",
        "## Non-Goals",
    ):
        assert section in markdown
    assert "Runtime, Strategy, paper trading, and broker execution use remain `NOT_AUTHORIZED`." in markdown


def test_write_plan_candidate_writes_json_without_overwrite(tmp_path: Path):
    result = planning.write_runtime_migration_plan_candidate_v1(tmp_path)

    assert result["artifact_kind"] == planning.ARTIFACT_KIND_RUNTIME_MIGRATION_PLAN_CANDIDATE
    assert result["payload_sha256"]
    with pytest.raises(planning.RuntimeMigrationPlanningError, match="already exists"):
        planning.write_runtime_migration_plan_candidate_v1(tmp_path)


def test_runtime_migration_planning_service_exports_are_public():
    import marketflow.services as services

    assert services.ARTIFACT_KIND_RUNTIME_MIGRATION_PLAN_CANDIDATE == "RUNTIME_MIGRATION_PLAN_CANDIDATE"
    assert services.RUNTIME_MIGRATION_PLAN_READY_FOR_OPERATOR_REVIEW == "RUNTIME_MIGRATION_PLAN_READY_FOR_OPERATOR_REVIEW"
    assert services.build_runtime_migration_plan_candidate_v1 is planning.build_runtime_migration_plan_candidate_v1
    assert services.validate_runtime_migration_plan_candidate_v1 is planning.validate_runtime_migration_plan_candidate_v1
    assert services.write_runtime_migration_plan_candidate_v1 is planning.write_runtime_migration_plan_candidate_v1
    assert services.build_runtime_migration_plan_markdown_v1 is planning.build_runtime_migration_plan_markdown_v1
