from __future__ import annotations

from pathlib import Path

import pytest

from marketflow.services import research_applicability_campaign_plan_operator_review_service as review


def _package() -> dict:
    return review.build_research_applicability_campaign_plan_candidate_review_package_v1()


def _profile(package: dict, profile: str) -> dict:
    return next(item for item in package["campaign_profiles"] if item["dataset_profile"] == profile)


def test_review_package_builds_offline_without_provider_calls(monkeypatch: pytest.MonkeyPatch):
    def fail_provider_call(*_args, **_kwargs):  # pragma: no cover
        raise AssertionError("provider path must not be called")

    monkeypatch.setattr(review.acquisition, "fetch_massive_custom_bars_v1", fail_provider_call)

    package = _package()

    assert package["created_offline"] is True
    assert package["provider_requests_made_in_review"] is False


def test_artifact_kind_is_campaign_plan_review_package():
    assert (
        _package()["artifact_kind"]
        == review.ARTIFACT_KIND_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_CANDIDATE_REVIEW_PACKAGE
    )


def test_review_status_is_ready():
    assert _package()["review_status"] == review.RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_CANDIDATE_REVIEW_PACKAGE_READY


def test_campaign_plan_digest_is_bound():
    assert _package()["reviewed_plan_digest"] == review.EXPECTED_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_DIGEST


def test_dataset_availability_review_digest_is_bound():
    assert (
        _package()["dataset_file_availability_verification_review_package_digest"]
        == review.campaign_plan.EXPECTED_DATASET_FILE_AVAILABILITY_VERIFICATION_REVIEW_PACKAGE_DIGEST
    )


def test_read_only_discovery_review_digest_is_bound():
    assert (
        _package()["read_only_discovery_review_package_digest"]
        == review.campaign_plan.EXPECTED_READ_ONLY_DISCOVERY_REVIEW_PACKAGE_DIGEST
    )


def test_runtime_migration_review_digest_is_bound():
    assert (
        _package()["runtime_migration_review_package_digest"]
        == review.campaign_plan.EXPECTED_RUNTIME_MIGRATION_REVIEW_PACKAGE_DIGEST
    )


def test_swing_registry_approval_digest_is_bound():
    assert (
        _package()["swing_registry_approval_digest"]
        == review.campaign_plan.availability_review.verification.discovery.runtime_planning.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST
    )


def test_position_swing_registry_approval_digest_is_bound():
    assert (
        _package()["position_swing_registry_approval_digest"]
        == review.campaign_plan.availability_review.verification.discovery.runtime_planning.EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST
    )


def test_campaign_scope_is_research_only():
    assert _package()["campaign_scope"] == "RESEARCH_ONLY"


def test_campaign_ticker_universe_is_aapl_only():
    assert _package()["campaign_ticker_universe"] == ["AAPL"]


def test_campaign_profiles_include_swing_and_position_swing():
    assert sorted(item["dataset_profile"] for item in _package()["campaign_profiles"]) == [
        "POSITION_SWING",
        "SWING",
    ]


def test_campaign_range_matches_requested_dates():
    package = _package()

    assert package["campaign_range_start"] == "2022-01-01"
    assert package["campaign_range_end"] == "2025-12-31"


def test_planned_questions_are_confirmed():
    assert _package()["campaign_questions"] == review.campaign_plan.CAMPAIGN_QUESTIONS


def test_planned_metrics_are_descriptive_research_only():
    package = _package()

    assert review._planned_metrics_descriptive_only(package["planned_metrics"]) is True


def test_future_execution_gates_are_defined():
    assert _package()["future_execution_gates"] == review.campaign_plan.FUTURE_EXECUTION_GATES


def test_risk_controls_are_defined():
    assert _package()["risk_controls"] == review.campaign_plan.RISK_CONTROLS


def test_touchpoint_inventory_is_present_and_incomplete_compact_acknowledged():
    package = _package()

    assert package["campaign_touchpoint_inventory"]
    assert package["campaign_touchpoint_inventory_count"] == 8
    assert package["campaign_touchpoint_inventory_status"] == review.CAMPAIGN_TOUCHPOINT_INVENTORY_INCOMPLETE_COMPACT


def test_campaign_execution_authorized_remains_false():
    assert _package()["campaign_execution_authorized"] is False


def test_campaign_execution_performed_remains_false():
    assert _package()["campaign_execution_performed"] is False


def test_provider_requests_made_in_review_remains_false():
    assert _package()["provider_requests_made_in_review"] is False


def test_runtime_migration_approved_remains_false():
    assert _package()["runtime_migration_approved"] is False


def test_runtime_migration_active_remains_false():
    assert _package()["runtime_migration_active"] is False


def test_strategy_runtime_migration_remains_false():
    assert _package()["strategy_runtime_migration"] is False


def test_runtime_use_remains_not_authorized():
    assert _package()["runtime_use"] == review.campaign_plan.NOT_AUTHORIZED


def test_strategy_use_remains_not_authorized():
    assert _package()["strategy_use"] == review.campaign_plan.NOT_AUTHORIZED


def test_paper_trading_remains_not_authorized():
    assert _package()["paper_trading"] == review.campaign_plan.NOT_AUTHORIZED


def test_broker_execution_remains_not_authorized():
    assert _package()["broker_execution"] == review.campaign_plan.NOT_AUTHORIZED


def test_automatic_stitching_remains_false():
    assert _package()["automatic_stitching"] is False


def test_predictive_usefulness_and_profitability_remain_not_accepted():
    package = _package()

    assert package["predictive_usefulness"] == review.acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED
    assert package["profitability"] == review.acquisition.PROFITABILITY_NOT_ACCEPTED


def test_checklist_contains_all_required_check_ids():
    assert [item["check_id"] for item in _package()["review_checklist"]] == review.REQUIRED_CHECK_IDS


def test_all_checks_pass_for_accepted_campaign_plan():
    assert {item["status"] for item in _package()["review_checklist"]} == {review.PASS}


def test_summary_counts_total_passed_failed_correctly():
    summary = _package()["review_summary"]

    assert summary["total_checks"] == len(review.REQUIRED_CHECK_IDS)
    assert summary["passed_checks"] == len(review.REQUIRED_CHECK_IDS)
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["ready_for_operator_assessment"] is True
    assert summary["software_campaign_execution_authorized"] is False
    assert summary["software_runtime_migration_authorized"] is False
    assert summary["software_runtime_activation_authorized"] is False


def test_review_package_digest_is_deterministic():
    first = _package()
    second = _package()

    assert first["research_applicability_campaign_plan_review_package_digest"] == second[
        "research_applicability_campaign_plan_review_package_digest"
    ]
    assert (
        first["research_applicability_campaign_plan_review_package_digest"]
        == review.research_applicability_campaign_plan_review_package_digest_v1(first)
    )


def test_validator_accepts_valid_review_package():
    validation = review.validate_research_applicability_campaign_plan_candidate_review_package_v1(_package())

    assert validation["status"] == "RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_CANDIDATE_REVIEW_PACKAGE_VALID"
    assert validation["campaign_execution_authorized"] is False


def test_validator_rejects_modified_campaign_plan_digest():
    package = _package()
    package["reviewed_plan_digest"] = "0" * 64

    with pytest.raises(review.ResearchApplicabilityCampaignPlanOperatorReviewError, match="reviewed_plan_digest"):
        review.validate_research_applicability_campaign_plan_candidate_review_package_v1(package)


def test_validator_rejects_non_research_scope():
    package = _package()
    package["campaign_scope"] = "RUNTIME"

    with pytest.raises(review.ResearchApplicabilityCampaignPlanOperatorReviewError, match="campaign_scope"):
        review.validate_research_applicability_campaign_plan_candidate_review_package_v1(package)


def test_validator_rejects_non_aapl_ticker_universe():
    package = _package()
    package["campaign_ticker_universe"] = ["AAPL", "MSFT"]

    with pytest.raises(review.ResearchApplicabilityCampaignPlanOperatorReviewError, match="campaign_ticker_universe"):
        review.validate_research_applicability_campaign_plan_candidate_review_package_v1(package)


def test_validator_rejects_missing_swing_profile():
    package = _package()
    position = _profile(package, "POSITION_SWING")
    package["campaign_profiles"] = [position, dict(position)]

    with pytest.raises(review.ResearchApplicabilityCampaignPlanOperatorReviewError, match="missing SWING"):
        review.validate_research_applicability_campaign_plan_candidate_review_package_v1(package)


def test_validator_rejects_missing_position_swing_profile():
    package = _package()
    swing = _profile(package, "SWING")
    package["campaign_profiles"] = [swing, dict(swing)]

    with pytest.raises(review.ResearchApplicabilityCampaignPlanOperatorReviewError, match="missing POSITION_SWING"):
        review.validate_research_applicability_campaign_plan_candidate_review_package_v1(package)


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("campaign_execution_authorized", True, "campaign_execution_authorized"),
        ("campaign_execution_performed", True, "campaign_execution_performed"),
        ("provider_requests_made_in_review", True, "provider_requests_made_in_review"),
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
    package = _package()
    package[field] = value

    with pytest.raises(review.ResearchApplicabilityCampaignPlanOperatorReviewError, match=match):
        review.validate_research_applicability_campaign_plan_candidate_review_package_v1(package)


def test_validator_rejects_predictive_and_profitability_accepted():
    for field in ("predictive_usefulness", "profitability"):
        package = _package()
        package[field] = "accepted"

        with pytest.raises(review.ResearchApplicabilityCampaignPlanOperatorReviewError, match=field):
            review.validate_research_applicability_campaign_plan_candidate_review_package_v1(package)


def test_validator_rejects_missing_future_gates():
    package = _package()
    package["future_execution_gates"] = []

    with pytest.raises(review.ResearchApplicabilityCampaignPlanOperatorReviewError, match="future_execution_gates"):
        review.validate_research_applicability_campaign_plan_candidate_review_package_v1(package)


def test_validator_rejects_missing_risk_controls():
    package = _package()
    package["risk_controls"] = []

    with pytest.raises(review.ResearchApplicabilityCampaignPlanOperatorReviewError, match="risk_controls"):
        review.validate_research_applicability_campaign_plan_candidate_review_package_v1(package)


def test_validator_rejects_wrong_artifact_kind():
    package = _package()
    package["artifact_kind"] = "WRONG"

    with pytest.raises(review.ResearchApplicabilityCampaignPlanOperatorReviewError, match="artifact_kind"):
        review.validate_research_applicability_campaign_plan_candidate_review_package_v1(package)


def test_validator_rejects_review_status_not_ready():
    package = _package()
    package["review_status"] = "BLOCKED"

    with pytest.raises(review.ResearchApplicabilityCampaignPlanOperatorReviewError, match="review_status"):
        review.validate_research_applicability_campaign_plan_candidate_review_package_v1(package)


def test_validator_rejects_missing_dataset_availability_review_digest():
    package = _package()
    package["dataset_file_availability_verification_review_package_digest"] = None

    with pytest.raises(
        review.ResearchApplicabilityCampaignPlanOperatorReviewError,
        match="dataset_file_availability_verification_review_package_digest",
    ):
        review.validate_research_applicability_campaign_plan_candidate_review_package_v1(package)


def test_validator_rejects_missing_read_only_discovery_review_digest():
    package = _package()
    package["read_only_discovery_review_package_digest"] = None

    with pytest.raises(
        review.ResearchApplicabilityCampaignPlanOperatorReviewError,
        match="read_only_discovery_review_package_digest",
    ):
        review.validate_research_applicability_campaign_plan_candidate_review_package_v1(package)


def test_validator_rejects_missing_runtime_migration_review_digest():
    package = _package()
    package["runtime_migration_review_package_digest"] = None

    with pytest.raises(
        review.ResearchApplicabilityCampaignPlanOperatorReviewError,
        match="runtime_migration_review_package_digest",
    ):
        review.validate_research_applicability_campaign_plan_candidate_review_package_v1(package)


def test_markdown_writer_includes_required_sections():
    markdown = review.build_research_applicability_campaign_plan_candidate_review_markdown_v1(_package())

    for section in (
        "## Title",
        "## Reviewed Research Applicability Campaign Plan",
        "## Campaign Scope",
        "## Research Dataset Inputs",
        "## Planned Questions",
        "## Planned Metrics",
        "## Future Execution Gates",
        "## Risk Controls",
        "## Runtime Boundary",
        "## Checklist Summary",
        "## Remaining Required Tasks",
        "## Guardrails",
    ):
        assert section in markdown


def test_write_review_package_writes_json_without_overwrite(tmp_path: Path):
    result = review.write_research_applicability_campaign_plan_candidate_review_package_v1(tmp_path)

    assert (
        result["artifact_kind"]
        == review.ARTIFACT_KIND_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_CANDIDATE_REVIEW_PACKAGE
    )
    assert result["payload_sha256"]
    with pytest.raises(review.ResearchApplicabilityCampaignPlanOperatorReviewError, match="already exists"):
        review.write_research_applicability_campaign_plan_candidate_review_package_v1(tmp_path)


def test_research_applicability_campaign_plan_review_service_exports_are_public():
    import marketflow.services as services

    assert (
        services.ARTIFACT_KIND_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_CANDIDATE_REVIEW_PACKAGE
        == "RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_CANDIDATE_REVIEW_PACKAGE"
    )
    assert (
        services.RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_CANDIDATE_REVIEW_PACKAGE_READY
        == "RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_CANDIDATE_REVIEW_PACKAGE_READY"
    )
    assert services.build_research_applicability_campaign_plan_candidate_review_package_v1 is review.build_research_applicability_campaign_plan_candidate_review_package_v1
    assert services.validate_research_applicability_campaign_plan_candidate_review_package_v1 is review.validate_research_applicability_campaign_plan_candidate_review_package_v1
    assert services.write_research_applicability_campaign_plan_candidate_review_package_v1 is review.write_research_applicability_campaign_plan_candidate_review_package_v1
    assert services.build_research_applicability_campaign_plan_candidate_review_markdown_v1 is review.build_research_applicability_campaign_plan_candidate_review_markdown_v1
