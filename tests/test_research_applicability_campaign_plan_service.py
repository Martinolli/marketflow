from __future__ import annotations

from pathlib import Path

import pytest

from marketflow.services import research_applicability_campaign_plan_service as plan_service


def _plan() -> dict:
    return plan_service.build_research_applicability_campaign_plan_candidate_v1()


def _profile(plan: dict, profile: str) -> dict:
    return next(item for item in plan["campaign_profiles"] if item["dataset_profile"] == profile)


def test_plan_candidate_builds_offline_without_provider_calls(monkeypatch: pytest.MonkeyPatch):
    def fail_provider_call(*_args, **_kwargs):  # pragma: no cover
        raise AssertionError("provider path must not be called")

    monkeypatch.setattr(plan_service.acquisition, "fetch_massive_custom_bars_v1", fail_provider_call)

    plan = _plan()

    assert plan["created_offline"] is True
    assert plan["provider_requests_made"] is False


def test_artifact_kind_is_research_applicability_campaign_plan_candidate():
    assert plan_service.ARTIFACT_KIND_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_CANDIDATE == _plan()["artifact_kind"]


def test_plan_status_is_ready_for_operator_review():
    assert _plan()["plan_status"] == plan_service.RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_READY_FOR_OPERATOR_REVIEW


def test_dataset_availability_review_digest_is_bound():
    assert (
        _plan()["dataset_file_availability_verification_review_package_digest"]
        == plan_service.EXPECTED_DATASET_FILE_AVAILABILITY_VERIFICATION_REVIEW_PACKAGE_DIGEST
    )


def test_read_only_discovery_review_digest_is_bound():
    assert (
        _plan()["read_only_discovery_review_package_digest"]
        == plan_service.EXPECTED_READ_ONLY_DISCOVERY_REVIEW_PACKAGE_DIGEST
    )


def test_runtime_migration_review_digest_is_bound():
    assert (
        _plan()["runtime_migration_review_package_digest"]
        == plan_service.EXPECTED_RUNTIME_MIGRATION_REVIEW_PACKAGE_DIGEST
    )


def test_swing_registry_approval_digest_is_bound():
    assert (
        _profile(_plan(), "SWING")["registry_approval_digest"]
        == plan_service.availability_review.verification.discovery.runtime_planning.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST
    )


def test_position_swing_registry_approval_digest_is_bound():
    assert (
        _profile(_plan(), "POSITION_SWING")["registry_approval_digest"]
        == plan_service.availability_review.verification.discovery.runtime_planning.EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST
    )


def test_campaign_ticker_universe_is_aapl_only():
    assert _plan()["campaign_ticker_universe"] == ["AAPL"]


def test_campaign_profiles_include_swing_and_position_swing():
    assert sorted(item["dataset_profile"] for item in _plan()["campaign_profiles"]) == [
        "POSITION_SWING",
        "SWING",
    ]


def test_campaign_execution_performed_remains_false():
    assert _plan()["campaign_execution_performed"] is False


def test_provider_requests_made_remains_false():
    assert _plan()["provider_requests_made"] is False


def test_runtime_migration_approved_remains_false():
    assert _plan()["runtime_migration_approved"] is False


def test_runtime_migration_active_remains_false():
    assert _plan()["runtime_migration_active"] is False


def test_strategy_runtime_migration_remains_false():
    assert _plan()["strategy_runtime_migration"] is False


def test_runtime_use_remains_not_authorized():
    assert _plan()["runtime_use"] == plan_service.NOT_AUTHORIZED


def test_strategy_use_remains_not_authorized():
    assert _plan()["strategy_use"] == plan_service.NOT_AUTHORIZED


def test_paper_trading_remains_not_authorized():
    assert _plan()["paper_trading"] == plan_service.NOT_AUTHORIZED


def test_broker_execution_remains_not_authorized():
    assert _plan()["broker_execution"] == plan_service.NOT_AUTHORIZED


def test_automatic_stitching_remains_false():
    assert _plan()["automatic_stitching"] is False


def test_predictive_usefulness_and_profitability_remain_not_accepted():
    plan = _plan()

    assert plan["predictive_usefulness"] == plan_service.acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED
    assert plan["profitability"] == plan_service.acquisition.PROFITABILITY_NOT_ACCEPTED


def test_future_execution_gates_are_defined():
    assert _plan()["operator_gates"] == plan_service.FUTURE_EXECUTION_GATES


def test_risk_controls_are_defined():
    assert _plan()["risk_controls"] == plan_service.RISK_CONTROLS


def test_planned_outputs_are_research_only():
    assert {
        output["status"] for output in _plan()["planned_outputs"]
    } == {plan_service.RESEARCH_ONLY_PLANNED_NOT_CREATED}


def test_campaign_touchpoint_inventory_is_present():
    plan = _plan()

    assert plan["campaign_touchpoint_inventory"]
    assert plan["campaign_touchpoint_inventory_complete"] is False


def test_checklist_contains_all_required_check_ids():
    assert [item["check_id"] for item in _plan()["plan_checklist"]] == plan_service.REQUIRED_CHECK_IDS


def test_all_checks_pass_for_accepted_plan():
    assert {item["status"] for item in _plan()["plan_checklist"]} == {plan_service.PASS}


def test_summary_counts_total_passed_failed_correctly():
    summary = _plan()["plan_summary"]

    assert summary["total_checks"] == len(plan_service.REQUIRED_CHECK_IDS)
    assert summary["passed_checks"] == len(plan_service.REQUIRED_CHECK_IDS)
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["campaign_execution_authorized"] is False
    assert summary["runtime_migration_authorized"] is False
    assert summary["software_runtime_activation_authorized"] is False


def test_plan_digest_is_deterministic():
    first = _plan()
    second = _plan()

    assert first["research_applicability_campaign_plan_digest"] == second[
        "research_applicability_campaign_plan_digest"
    ]
    assert (
        first["research_applicability_campaign_plan_digest"]
        == plan_service.research_applicability_campaign_plan_digest_v1(first)
    )


def test_validator_accepts_valid_plan():
    validation = plan_service.validate_research_applicability_campaign_plan_candidate_v1(_plan())

    assert validation["status"] == "RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_CANDIDATE_VALID"
    assert validation["campaign_execution_authorized"] is False


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("campaign_execution_performed", True, "campaign_execution_performed"),
        ("provider_requests_made", True, "provider_requests_made"),
        ("runtime_migration_approved", True, "runtime_migration_approved"),
        ("runtime_migration_active", True, "runtime_migration_active"),
        ("strategy_runtime_migration", True, "strategy_runtime_migration"),
        ("runtime_use", "AUTHORIZED", "runtime_use"),
        ("strategy_use", "AUTHORIZED", "strategy_use"),
        ("paper_trading", "AUTHORIZED", "paper_trading"),
        ("broker_execution", "AUTHORIZED", "broker_execution"),
    ],
)
def test_validator_rejects_forbidden_boundary_mutations(field: str, value, match: str):
    plan = _plan()
    plan[field] = value

    with pytest.raises(plan_service.ResearchApplicabilityCampaignPlanError, match=match):
        plan_service.validate_research_applicability_campaign_plan_candidate_v1(plan)


def test_validator_rejects_predictive_and_profitability_accepted():
    for field in ("predictive_usefulness", "profitability"):
        plan = _plan()
        plan[field] = "accepted"

        with pytest.raises(plan_service.ResearchApplicabilityCampaignPlanError, match=field):
            plan_service.validate_research_applicability_campaign_plan_candidate_v1(plan)


def test_validator_rejects_non_aapl_ticker_universe():
    plan = _plan()
    plan["campaign_ticker_universe"] = ["AAPL", "MSFT"]

    with pytest.raises(plan_service.ResearchApplicabilityCampaignPlanError, match="campaign_ticker_universe"):
        plan_service.validate_research_applicability_campaign_plan_candidate_v1(plan)


def test_validator_rejects_missing_future_gates():
    plan = _plan()
    plan["operator_gates"] = []

    with pytest.raises(plan_service.ResearchApplicabilityCampaignPlanError, match="operator_gates"):
        plan_service.validate_research_applicability_campaign_plan_candidate_v1(plan)


def test_validator_rejects_missing_risk_controls():
    plan = _plan()
    plan["risk_controls"] = []

    with pytest.raises(plan_service.ResearchApplicabilityCampaignPlanError, match="risk_controls"):
        plan_service.validate_research_applicability_campaign_plan_candidate_v1(plan)


def test_validator_rejects_wrong_artifact_kind():
    plan = _plan()
    plan["artifact_kind"] = "WRONG"

    with pytest.raises(plan_service.ResearchApplicabilityCampaignPlanError, match="artifact_kind"):
        plan_service.validate_research_applicability_campaign_plan_candidate_v1(plan)


def test_validator_rejects_missing_swing_registry_approval_digest():
    plan = _plan()
    _profile(plan, "SWING")["registry_approval_digest"] = None

    with pytest.raises(plan_service.ResearchApplicabilityCampaignPlanError, match="registry_approval_digest"):
        plan_service.validate_research_applicability_campaign_plan_candidate_v1(plan)


def test_validator_rejects_missing_position_swing_registry_approval_digest():
    plan = _plan()
    _profile(plan, "POSITION_SWING")["registry_approval_digest"] = None

    with pytest.raises(plan_service.ResearchApplicabilityCampaignPlanError, match="registry_approval_digest"):
        plan_service.validate_research_applicability_campaign_plan_candidate_v1(plan)


def test_validator_rejects_missing_dataset_availability_review_digest():
    plan = _plan()
    plan["dataset_file_availability_verification_review_package_digest"] = None

    with pytest.raises(
        plan_service.ResearchApplicabilityCampaignPlanError,
        match="dataset_file_availability_verification_review_package_digest",
    ):
        plan_service.validate_research_applicability_campaign_plan_candidate_v1(plan)


def test_validator_rejects_missing_plan_digest():
    plan = _plan()
    plan.pop("research_applicability_campaign_plan_digest")

    with pytest.raises(plan_service.ResearchApplicabilityCampaignPlanError, match="research_applicability_campaign_plan_digest"):
        plan_service.validate_research_applicability_campaign_plan_candidate_v1(plan)


def test_markdown_writer_includes_required_sections():
    markdown = plan_service.build_research_applicability_campaign_plan_markdown_v1(_plan())

    for section in (
        "## Title",
        "## Purpose",
        "## Research Dataset Inputs",
        "## Campaign Scope",
        "## Campaign Questions",
        "## Planned Metrics",
        "## Planned Outputs",
        "## Future Execution Gates",
        "## Risk Controls",
        "## Campaign Touchpoint Inventory",
        "## Checklist Summary",
        "## Runtime Boundary",
        "## Non-Goals",
    ):
        assert section in markdown


def test_write_plan_candidate_writes_json_without_overwrite(tmp_path: Path):
    result = plan_service.write_research_applicability_campaign_plan_candidate_v1(tmp_path)

    assert result["artifact_kind"] == plan_service.ARTIFACT_KIND_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_CANDIDATE
    assert result["payload_sha256"]
    with pytest.raises(plan_service.ResearchApplicabilityCampaignPlanError, match="already exists"):
        plan_service.write_research_applicability_campaign_plan_candidate_v1(tmp_path)


def test_research_applicability_campaign_plan_service_exports_are_public():
    import marketflow.services as services

    assert (
        services.ARTIFACT_KIND_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_CANDIDATE
        == "RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_CANDIDATE"
    )
    assert (
        services.RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_READY_FOR_OPERATOR_REVIEW
        == "RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_READY_FOR_OPERATOR_REVIEW"
    )
    assert services.build_research_applicability_campaign_plan_candidate_v1 is plan_service.build_research_applicability_campaign_plan_candidate_v1
    assert services.validate_research_applicability_campaign_plan_candidate_v1 is plan_service.validate_research_applicability_campaign_plan_candidate_v1
    assert services.write_research_applicability_campaign_plan_candidate_v1 is plan_service.write_research_applicability_campaign_plan_candidate_v1
    assert services.build_research_applicability_campaign_plan_markdown_v1 is plan_service.build_research_applicability_campaign_plan_markdown_v1
