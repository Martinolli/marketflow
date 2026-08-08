from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from marketflow.services import runtime_migration_operator_review_service as review
from marketflow.services import runtime_migration_planning_service as planning


def _package() -> dict:
    return review.build_runtime_migration_plan_candidate_review_package_v1()


def test_review_package_builds_offline_without_provider_calls(monkeypatch: pytest.MonkeyPatch):
    def fail_provider_call(*_args, **_kwargs):  # pragma: no cover
        raise AssertionError("provider path must not be called")

    monkeypatch.setattr(review.planning.acquisition, "fetch_massive_custom_bars_v1", fail_provider_call)

    package = _package()

    assert package["created_offline"] is True
    assert package["provider_requests_made_in_review"] is False
    assert package["binding_mode"] == review.RUNTIME_MIGRATION_PLAN_STATUS_BINDING


def test_review_package_artifact_kind_and_status_are_review_only():
    package = _package()

    assert package["artifact_kind"] == review.ARTIFACT_KIND_RUNTIME_MIGRATION_PLAN_CANDIDATE_REVIEW_PACKAGE
    assert package["review_status"] == review.RUNTIME_MIGRATION_PLAN_CANDIDATE_REVIEW_PACKAGE_READY
    assert package["artifact_kind"] != "RUNTIME_MIGRATION_APPROVED"
    assert package["review_status"] != "RUNTIME_MIGRATION_APPROVED"


def test_review_package_binds_runtime_plan_and_registry_digests():
    package = _package()

    assert package["reviewed_plan_digest"] == review.EXPECTED_RUNTIME_MIGRATION_PLAN_DIGEST
    assert package["swing_registry_approval_digest"] == planning.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST
    assert (
        package["position_swing_registry_approval_digest"]
        == planning.EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST
    )


def test_review_package_keeps_all_runtime_authority_not_authorized():
    package = _package()

    assert package["runtime_migration_approved"] is False
    assert package["runtime_migration_active"] is False
    assert package["strategy_runtime_migration"] is False
    assert package["automatic_stitching"] is False
    assert package["runtime_use"] == planning.NOT_AUTHORIZED
    assert package["strategy_use"] == planning.NOT_AUTHORIZED
    assert package["paper_trading"] == planning.NOT_AUTHORIZED
    assert package["broker_execution"] == planning.NOT_AUTHORIZED
    assert package["swing_runtime_use"] == planning.NOT_AUTHORIZED
    assert package["swing_strategy_use"] == planning.NOT_AUTHORIZED
    assert package["position_swing_runtime_use"] == planning.NOT_AUTHORIZED
    assert package["position_swing_strategy_use"] == planning.NOT_AUTHORIZED
    assert package["predictive_usefulness"] == review.acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED
    assert package["profitability"] == review.acquisition.PROFITABILITY_NOT_ACCEPTED


def test_review_package_confirms_planned_phases_future_gates_and_guardrails():
    package = _package()

    assert package["planned_phases"] == planning.PLANNED_PHASES
    assert package["future_gates"] == planning.FUTURE_GATES
    assert package["hard_guardrails"] == planning.HARD_GUARDRAILS


def test_review_package_acknowledges_compact_incomplete_touchpoint_inventory():
    package = _package()

    assert package["runtime_touchpoint_inventory"]
    assert package["runtime_touchpoint_inventory_count"] == 10
    assert package["runtime_touchpoint_inventory_status"] == review.RUNTIME_TOUCHPOINT_INVENTORY_INCOMPLETE_COMPACT


def test_review_checklist_contains_required_ids_and_all_passes():
    package = _package()

    assert [item["check_id"] for item in package["review_checklist"]] == review.REQUIRED_CHECK_IDS
    assert {item["status"] for item in package["review_checklist"]} == {review.PASS}


def test_review_summary_counts_total_passed_failed_and_blockers():
    package = _package()
    summary = package["review_summary"]

    assert summary["total_checks"] == len(review.REQUIRED_CHECK_IDS)
    assert summary["passed_checks"] == len(review.REQUIRED_CHECK_IDS)
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["ready_for_operator_assessment"] is True
    assert summary["operator_decision_required_before_runtime_migration"] is True
    assert summary["software_runtime_migration_authorized"] is False
    assert summary["software_runtime_activation_authorized"] is False


def test_review_package_digest_is_deterministic():
    first = _package()
    second = _package()

    assert first["runtime_migration_review_package_digest"] == second["runtime_migration_review_package_digest"]
    assert (
        first["runtime_migration_review_package_digest"]
        == review.runtime_migration_review_package_digest_v1(first)
    )


def test_review_validator_accepts_valid_package():
    validation = review.validate_runtime_migration_plan_candidate_review_package_v1(_package())

    assert validation["status"] == "RUNTIME_MIGRATION_PLAN_CANDIDATE_REVIEW_PACKAGE_VALID"
    assert validation["runtime_migration_approved"] is False
    assert validation["runtime_migration_active"] is False
    assert validation["strategy_runtime_migration"] is False
    assert validation["total_checks"] == len(review.REQUIRED_CHECK_IDS)
    assert validation["blocker_count"] == 0


def test_review_package_can_bind_supplied_plan_object():
    plan = planning.build_runtime_migration_plan_candidate_v1()

    package = review.build_runtime_migration_plan_candidate_review_package_v1(plan)

    assert package["binding_mode"] == review.RUNTIME_MIGRATION_PLAN_OBJECT_BINDING
    assert package["reviewed_plan_digest"] == review.EXPECTED_RUNTIME_MIGRATION_PLAN_DIGEST


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("artifact_kind", "WRONG", "artifact_kind"),
        ("review_status", "WRONG", "review_status"),
        ("reviewed_plan_digest", "0" * 64, "reviewed_plan_digest"),
        ("swing_registry_approval_digest", None, "swing_registry_approval_digest"),
        ("position_swing_registry_approval_digest", None, "position_swing_registry_approval_digest"),
        ("runtime_migration_approved", True, "runtime_migration_approved"),
        ("runtime_migration_active", True, "runtime_migration_active"),
        ("strategy_runtime_migration", True, "strategy_runtime_migration"),
        ("runtime_use", "AUTHORIZED", "runtime_use"),
        ("strategy_use", "AUTHORIZED", "strategy_use"),
        ("paper_trading", "AUTHORIZED", "paper_trading"),
        ("broker_execution", "AUTHORIZED", "broker_execution"),
        ("automatic_stitching", True, "automatic_stitching"),
        ("predictive_usefulness", "accepted", "predictive_usefulness"),
        ("profitability", "accepted", "profitability"),
        ("planned_phases", [], "planned_phases"),
        ("future_gates", [], "future_gates"),
        ("hard_guardrails", [], "hard_guardrails"),
        ("provider_requests_made_in_review", True, "provider_requests_made_in_review"),
        ("approval_status", "RUNTIME_MIGRATION_APPROVED", "approval_status"),
    ],
)
def test_review_validator_rejects_invalid_mutations(field: str, value, match: str):
    package = _package()
    package[field] = value

    with pytest.raises(review.RuntimeMigrationOperatorReviewError, match=match):
        review.validate_runtime_migration_plan_candidate_review_package_v1(package)


def test_review_validator_rejects_missing_touchpoint_inventory():
    package = _package()
    package["runtime_touchpoint_inventory"] = []

    with pytest.raises(review.RuntimeMigrationOperatorReviewError, match="runtime_touchpoint_inventory"):
        review.validate_runtime_migration_plan_candidate_review_package_v1(package)


def test_review_validator_rejects_runtime_migration_approval_status_values():
    for field in ("artifact_kind", "review_status"):
        package = _package()
        package[field] = "RUNTIME_MIGRATION_APPROVED"

        with pytest.raises(review.RuntimeMigrationOperatorReviewError, match="RUNTIME_MIGRATION_APPROVED"):
            review.validate_runtime_migration_plan_candidate_review_package_v1(package)


def test_review_validator_rejects_runtime_active_and_strategy_migration_status_values():
    for field, status in (
        ("review_status", "RUNTIME_MIGRATION_ACTIVE"),
        ("review_status", "STRATEGY_RUNTIME_MIGRATION"),
    ):
        package = _package()
        package[field] = status

        with pytest.raises(review.RuntimeMigrationOperatorReviewError, match=status):
            review.validate_runtime_migration_plan_candidate_review_package_v1(package)


def test_review_validator_rejects_mutated_digest():
    package = _package()
    package["runtime_migration_review_package_digest"] = "0" * 64

    with pytest.raises(review.RuntimeMigrationOperatorReviewError, match="runtime_migration_review_package_digest"):
        review.validate_runtime_migration_plan_candidate_review_package_v1(package)


def test_review_validator_rejects_mutated_checklist():
    package = _package()
    package["review_checklist"] = deepcopy(package["review_checklist"])
    package["review_checklist"][0]["status"] = review.FAIL

    with pytest.raises(review.RuntimeMigrationOperatorReviewError, match="review_checklist"):
        review.validate_runtime_migration_plan_candidate_review_package_v1(package)


def test_review_markdown_includes_required_sections_and_guardrails():
    markdown = review.build_runtime_migration_plan_candidate_review_markdown_v1(_package())

    for section in (
        "## Title",
        "## Reviewed Runtime Migration Plan",
        "## Registry Inputs",
        "## Runtime Boundary",
        "## Planned Phases",
        "## Future Gates",
        "## Hard Guardrails",
        "## Touchpoint Inventory Note",
        "## Checklist Summary",
        "## Remaining Required Tasks",
        "## Guardrails",
        "## Review Package Digest",
    ):
        assert section in markdown
    assert "Runtime, Strategy, paper trading, and broker execution use remain `NOT_AUTHORIZED`." in markdown
    assert "Predictive usefulness and profitability remain not accepted." in markdown


def test_write_review_package_writes_json_without_overwrite(tmp_path: Path):
    result = review.write_runtime_migration_plan_candidate_review_package_v1(tmp_path)

    assert result["artifact_kind"] == review.ARTIFACT_KIND_RUNTIME_MIGRATION_PLAN_CANDIDATE_REVIEW_PACKAGE
    assert result["payload_sha256"]
    with pytest.raises(review.RuntimeMigrationOperatorReviewError, match="already exists"):
        review.write_runtime_migration_plan_candidate_review_package_v1(tmp_path)


def test_runtime_migration_operator_review_service_exports_are_public():
    import marketflow.services as services

    assert (
        services.ARTIFACT_KIND_RUNTIME_MIGRATION_PLAN_CANDIDATE_REVIEW_PACKAGE
        == "RUNTIME_MIGRATION_PLAN_CANDIDATE_REVIEW_PACKAGE"
    )
    assert (
        services.RUNTIME_MIGRATION_PLAN_CANDIDATE_REVIEW_PACKAGE_READY
        == "RUNTIME_MIGRATION_PLAN_CANDIDATE_REVIEW_PACKAGE_READY"
    )
    assert (
        services.build_runtime_migration_plan_candidate_review_package_v1
        is review.build_runtime_migration_plan_candidate_review_package_v1
    )
    assert (
        services.validate_runtime_migration_plan_candidate_review_package_v1
        is review.validate_runtime_migration_plan_candidate_review_package_v1
    )
    assert (
        services.write_runtime_migration_plan_candidate_review_package_v1
        is review.write_runtime_migration_plan_candidate_review_package_v1
    )
    assert (
        services.build_runtime_migration_plan_candidate_review_markdown_v1
        is review.build_runtime_migration_plan_candidate_review_markdown_v1
    )
    assert services.runtime_migration_review_package_digest_v1 is review.runtime_migration_review_package_digest_v1
