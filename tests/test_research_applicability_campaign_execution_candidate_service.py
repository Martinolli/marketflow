from __future__ import annotations

from pathlib import Path

import pytest

from marketflow.services import research_applicability_campaign_execution_candidate_service as execution


def _candidate() -> dict:
    return execution.build_research_applicability_campaign_execution_candidate_v1()


def _input(candidate: dict, profile: str) -> dict:
    return next(item for item in candidate["planned_inputs"] if item["dataset_profile"] == profile)


def test_execution_candidate_builds_offline_without_provider_calls(monkeypatch: pytest.MonkeyPatch):
    def fail_provider_call(*_args, **_kwargs):  # pragma: no cover
        raise AssertionError("provider path must not be called")

    monkeypatch.setattr(execution.acquisition, "fetch_massive_custom_bars_v1", fail_provider_call)

    candidate = _candidate()

    assert candidate["created_offline"] is True
    assert candidate["provider_requests_made"] is False


def test_artifact_kind_is_execution_candidate():
    assert (
        _candidate()["artifact_kind"]
        == execution.ARTIFACT_KIND_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_CANDIDATE
    )


def test_candidate_status_is_ready_for_operator_review():
    assert (
        _candidate()["candidate_status"]
        == execution.RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_READY_FOR_OPERATOR_REVIEW
    )


def test_campaign_execution_request_id_is_deterministic():
    assert _candidate()["campaign_execution_request_id"] == execution.CAMPAIGN_EXECUTION_REQUEST_ID


def test_campaign_plan_and_review_digests_are_bound():
    candidate = _candidate()

    assert (
        candidate["research_campaign_plan_digest"]
        == execution.EXPECTED_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_DIGEST
    )
    assert (
        candidate["research_campaign_plan_review_package_digest"]
        == execution.EXPECTED_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_REVIEW_PACKAGE_DIGEST
    )


def test_dataset_availability_review_digest_is_bound():
    assert (
        _candidate()["dataset_file_availability_verification_review_package_digest"]
        == execution.EXPECTED_DATASET_FILE_AVAILABILITY_VERIFICATION_REVIEW_PACKAGE_DIGEST
    )


def test_discovery_and_runtime_review_digests_are_bound():
    candidate = _candidate()

    assert (
        candidate["read_only_discovery_review_package_digest"]
        == execution.EXPECTED_READ_ONLY_DISCOVERY_REVIEW_PACKAGE_DIGEST
    )
    assert (
        candidate["runtime_migration_review_package_digest"]
        == execution.EXPECTED_RUNTIME_MIGRATION_REVIEW_PACKAGE_DIGEST
    )


def test_registry_approval_digests_are_bound():
    candidate = _candidate()

    assert (
        candidate["swing_registry_approval_digest"]
        == execution.plan_review.campaign_plan.availability_review.verification.discovery.runtime_planning.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST
    )
    assert (
        candidate["position_swing_registry_approval_digest"]
        == execution.plan_review.campaign_plan.availability_review.verification.discovery.runtime_planning.EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST
    )


def test_campaign_scope_matches_request():
    candidate = _candidate()

    assert candidate["campaign_scope"] == "RESEARCH_ONLY"
    assert candidate["ticker_universe"] == ["AAPL"]
    assert candidate["dataset_profiles"] == ["SWING", "POSITION_SWING"]
    assert candidate["date_range_start"] == "2022-01-01"
    assert candidate["date_range_end"] == "2025-12-31"


def test_modes_remain_research_only_disabled():
    candidate = _candidate()

    assert candidate["execution_mode"] == execution.READ_ONLY_OFFLINE_RESEARCH
    assert candidate["runtime_mode"] == execution.NOT_RUNTIME
    assert candidate["strategy_mode"] == execution.NOT_STRATEGY_INPUT
    assert candidate["broker_mode"] == execution.DISABLED
    assert candidate["paper_trading_mode"] == execution.DISABLED


def test_nested_campaign_execution_request_matches_top_level_fields():
    candidate = _candidate()

    assert candidate["campaign_execution_request"] == {
        "campaign_execution_request_id": candidate["campaign_execution_request_id"],
        "campaign_name": candidate["campaign_name"],
        "campaign_scope": candidate["campaign_scope"],
        "ticker_universe": candidate["ticker_universe"],
        "dataset_profiles": candidate["dataset_profiles"],
        "date_range_start": candidate["date_range_start"],
        "date_range_end": candidate["date_range_end"],
        "execution_mode": candidate["execution_mode"],
        "runtime_mode": candidate["runtime_mode"],
        "strategy_mode": candidate["strategy_mode"],
        "broker_mode": candidate["broker_mode"],
        "paper_trading_mode": candidate["paper_trading_mode"],
    }


def test_planned_inputs_include_swing_and_position_swing():
    assert sorted(item["dataset_profile"] for item in _candidate()["planned_inputs"]) == [
        "POSITION_SWING",
        "SWING",
    ]


def test_planned_inputs_are_read_only_and_not_authorized():
    candidate = _candidate()

    for profile in candidate["planned_inputs"]:
        assert profile["load_mode"] == "READ_ONLY"
        assert profile["runtime_use"] == execution.NOT_AUTHORIZED
        assert profile["strategy_use"] == execution.NOT_AUTHORIZED
        assert profile["dataset_generation_allowed"] is False
        assert profile["provider_refresh_allowed"] is False


def test_swing_planned_dataset_path_is_bound():
    assert (
        _input(_candidate(), "SWING")["planned_dataset_path"]
        == ".marketflow/canonical_candidates/AAPL/SWING/AAPL_SWING_RTH_HALF_SESSION_195M_2022_2025.csv"
    )


def test_position_swing_planned_dataset_path_is_bound():
    assert (
        _input(_candidate(), "POSITION_SWING")["planned_dataset_path"]
        == ".marketflow/canonical_candidates/AAPL/POSITION_SWING/AAPL_POSITION_SWING_RTH_FULL_SESSION_1D_2022_2025.csv"
    )


def test_planned_outputs_are_not_generated_and_research_only():
    candidate = _candidate()

    assert [output["name"] for output in candidate["planned_outputs"]] == execution.PLANNED_OUTPUT_NAMES
    assert candidate["planned_output_root"] == execution.PLANNED_OUTPUT_ROOT
    for output in candidate["planned_outputs"]:
        assert output["status"] == execution.PLANNED_NOT_GENERATED
        assert output["generated"] is False
        assert output["output_label"] == execution.RESEARCH_ONLY_NON_ACTIONABLE


def test_planned_execution_phases_are_not_performed():
    candidate = _candidate()

    assert [phase["action"] for phase in candidate["planned_execution_phases"]] == execution.PLANNED_EXECUTION_PHASES
    for phase in candidate["planned_execution_phases"]:
        assert phase["execution_performed"] is False
        assert phase["output_generated"] is False
        assert phase["output_label"] == execution.RESEARCH_ONLY_NON_ACTIONABLE


def test_execution_gates_are_defined():
    assert _candidate()["execution_gates"] == execution.EXECUTION_GATES


def test_risk_controls_are_defined():
    assert _candidate()["risk_controls"] == execution.RISK_CONTROLS


def test_no_campaign_execution_or_results_are_authorized():
    candidate = _candidate()

    assert candidate["campaign_execution_authorized"] is False
    assert candidate["campaign_execution_performed"] is False
    assert candidate["campaign_results_generated"] is False


def test_runtime_migration_and_strategy_runtime_migration_remain_false():
    candidate = _candidate()

    assert candidate["runtime_migration_approved"] is False
    assert candidate["runtime_migration_active"] is False
    assert candidate["strategy_runtime_migration"] is False


def test_runtime_strategy_paper_and_broker_use_remain_not_authorized():
    candidate = _candidate()

    assert candidate["runtime_use"] == execution.NOT_AUTHORIZED
    assert candidate["strategy_use"] == execution.NOT_AUTHORIZED
    assert candidate["paper_trading"] == execution.NOT_AUTHORIZED
    assert candidate["broker_execution"] == execution.NOT_AUTHORIZED


def test_automatic_stitching_remains_false():
    assert _candidate()["automatic_stitching"] is False


def test_predictive_usefulness_and_profitability_remain_not_accepted():
    candidate = _candidate()

    assert candidate["predictive_usefulness"] == execution.acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED
    assert candidate["profitability"] == execution.acquisition.PROFITABILITY_NOT_ACCEPTED


def test_checklist_contains_all_required_check_ids():
    assert [item["check_id"] for item in _candidate()["candidate_checklist"]] == execution.REQUIRED_CHECK_IDS


def test_all_checks_pass_for_candidate():
    assert {item["status"] for item in _candidate()["candidate_checklist"]} == {execution.PASS}


def test_summary_counts_total_passed_failed_correctly():
    summary = _candidate()["candidate_summary"]

    assert summary["total_checks"] == len(execution.REQUIRED_CHECK_IDS)
    assert summary["passed_checks"] == len(execution.REQUIRED_CHECK_IDS)
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["ready_for_operator_review"] is True
    assert summary["campaign_execution_authorized"] is False
    assert summary["campaign_execution_performed"] is False
    assert summary["runtime_migration_authorized"] is False
    assert summary["software_runtime_activation_authorized"] is False


def test_execution_candidate_digest_is_deterministic():
    first = _candidate()
    second = _candidate()

    assert first["research_applicability_campaign_execution_candidate_digest"] == second[
        "research_applicability_campaign_execution_candidate_digest"
    ]
    assert (
        first["research_applicability_campaign_execution_candidate_digest"]
        == execution.research_applicability_campaign_execution_candidate_digest_v1(first)
    )


def test_validator_accepts_valid_execution_candidate():
    validation = execution.validate_research_applicability_campaign_execution_candidate_v1(_candidate())

    assert validation["status"] == "RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_CANDIDATE_VALID"
    assert validation["campaign_execution_authorized"] is False
    assert validation["campaign_execution_performed"] is False
    assert validation["campaign_results_generated"] is False


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("provider_requests_made", True, "provider_requests_made"),
        ("campaign_execution_authorized", True, "campaign_execution_authorized"),
        ("campaign_execution_performed", True, "campaign_execution_performed"),
        ("campaign_results_generated", True, "campaign_results_generated"),
        ("runtime_migration_approved", True, "runtime_migration_approved"),
        ("runtime_migration_active", True, "runtime_migration_active"),
        ("strategy_runtime_migration", True, "strategy_runtime_migration"),
        ("runtime_use", "AUTHORIZED", "runtime_use"),
        ("strategy_use", "AUTHORIZED", "strategy_use"),
        ("paper_trading", "AUTHORIZED", "paper_trading"),
        ("broker_execution", "AUTHORIZED", "broker_execution"),
        ("automatic_stitching", True, "automatic_stitching"),
    ],
)
def test_validator_rejects_forbidden_boundary_mutations(field: str, value, match: str):
    candidate = _candidate()
    candidate[field] = value

    with pytest.raises(execution.ResearchApplicabilityCampaignExecutionCandidateError, match=match):
        execution.validate_research_applicability_campaign_execution_candidate_v1(candidate)


@pytest.mark.parametrize(
    "forbidden_value",
    [
        "RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTED",
        "RESEARCH_APPLICABILITY_CAMPAIGN_RESULTS",
        "PREDICTIVE_USEFULNESS_ACCEPTED",
        "PROFITABILITY_ACCEPTED",
        "RUNTIME_MIGRATION_APPROVED",
        "RUNTIME_MIGRATION_ACTIVE",
        "STRATEGY_RUNTIME_MIGRATION",
    ],
)
def test_validator_rejects_forbidden_status_literals(forbidden_value: str):
    candidate = _candidate()
    candidate["forbidden_marker"] = forbidden_value

    with pytest.raises(execution.ResearchApplicabilityCampaignExecutionCandidateError, match=forbidden_value):
        execution.validate_research_applicability_campaign_execution_candidate_v1(candidate)


def test_validator_rejects_predictive_and_profitability_accepted():
    for field in ("predictive_usefulness", "profitability"):
        candidate = _candidate()
        candidate[field] = "accepted"

        with pytest.raises(execution.ResearchApplicabilityCampaignExecutionCandidateError, match=field):
            execution.validate_research_applicability_campaign_execution_candidate_v1(candidate)


def test_validator_rejects_campaign_execution_request_authorization_mutation():
    candidate = _candidate()
    candidate["campaign_execution_request"]["execution_mode"] = "RUNTIME"

    with pytest.raises(execution.ResearchApplicabilityCampaignExecutionCandidateError, match="campaign_execution_request"):
        execution.validate_research_applicability_campaign_execution_candidate_v1(candidate)


def test_validator_rejects_non_aapl_ticker_universe():
    candidate = _candidate()
    candidate["ticker_universe"] = ["AAPL", "MSFT"]

    with pytest.raises(execution.ResearchApplicabilityCampaignExecutionCandidateError, match="ticker_universe"):
        execution.validate_research_applicability_campaign_execution_candidate_v1(candidate)


def test_validator_rejects_missing_swing_planned_input():
    candidate = _candidate()
    position = _input(candidate, "POSITION_SWING")
    candidate["planned_inputs"] = [position, dict(position)]

    with pytest.raises(execution.ResearchApplicabilityCampaignExecutionCandidateError, match="planned_inputs"):
        execution.validate_research_applicability_campaign_execution_candidate_v1(candidate)


def test_validator_rejects_missing_position_swing_planned_input():
    candidate = _candidate()
    swing = _input(candidate, "SWING")
    candidate["planned_inputs"] = [swing, dict(swing)]

    with pytest.raises(execution.ResearchApplicabilityCampaignExecutionCandidateError, match="planned_inputs"):
        execution.validate_research_applicability_campaign_execution_candidate_v1(candidate)


def test_validator_rejects_generated_planned_output():
    candidate = _candidate()
    candidate["planned_outputs"][0]["generated"] = True

    with pytest.raises(execution.ResearchApplicabilityCampaignExecutionCandidateError, match="generated"):
        execution.validate_research_applicability_campaign_execution_candidate_v1(candidate)


def test_validator_rejects_performed_execution_phase():
    candidate = _candidate()
    candidate["planned_execution_phases"][0]["execution_performed"] = True

    with pytest.raises(execution.ResearchApplicabilityCampaignExecutionCandidateError, match="execution_performed"):
        execution.validate_research_applicability_campaign_execution_candidate_v1(candidate)


def test_validator_rejects_missing_execution_gates():
    candidate = _candidate()
    candidate["execution_gates"] = []

    with pytest.raises(execution.ResearchApplicabilityCampaignExecutionCandidateError, match="execution_gates"):
        execution.validate_research_applicability_campaign_execution_candidate_v1(candidate)


def test_validator_rejects_missing_risk_controls():
    candidate = _candidate()
    candidate["risk_controls"] = []

    with pytest.raises(execution.ResearchApplicabilityCampaignExecutionCandidateError, match="risk_controls"):
        execution.validate_research_applicability_campaign_execution_candidate_v1(candidate)


def test_validator_rejects_wrong_artifact_kind():
    candidate = _candidate()
    candidate["artifact_kind"] = "WRONG"

    with pytest.raises(execution.ResearchApplicabilityCampaignExecutionCandidateError, match="artifact_kind"):
        execution.validate_research_applicability_campaign_execution_candidate_v1(candidate)


def test_validator_rejects_candidate_status_not_ready():
    candidate = _candidate()
    candidate["candidate_status"] = "RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTED"

    with pytest.raises(execution.ResearchApplicabilityCampaignExecutionCandidateError, match="candidate_status"):
        execution.validate_research_applicability_campaign_execution_candidate_v1(candidate)


def test_validator_rejects_modified_plan_review_digest():
    candidate = _candidate()
    candidate["research_campaign_plan_review_package_digest"] = "0" * 64

    with pytest.raises(
        execution.ResearchApplicabilityCampaignExecutionCandidateError,
        match="research_campaign_plan_review_package_digest",
    ):
        execution.validate_research_applicability_campaign_execution_candidate_v1(candidate)


def test_validator_rejects_missing_candidate_digest():
    candidate = _candidate()
    candidate.pop("research_applicability_campaign_execution_candidate_digest")

    with pytest.raises(
        execution.ResearchApplicabilityCampaignExecutionCandidateError,
        match="research_applicability_campaign_execution_candidate_digest",
    ):
        execution.validate_research_applicability_campaign_execution_candidate_v1(candidate)


def test_markdown_writer_includes_required_sections():
    markdown = execution.build_research_applicability_campaign_execution_candidate_markdown_v1(_candidate())

    for section in (
        "## Title",
        "## Candidate",
        "## Bound Source Evidence",
        "## Campaign Scope",
        "## Planned Inputs",
        "## Planned Outputs",
        "## Planned Execution Phases",
        "## Execution Gates",
        "## Risk Controls",
        "## Runtime Boundary",
        "## Checklist Summary",
        "## Non-Goals",
        "## Candidate Digest",
    ):
        assert section in markdown


def test_write_execution_candidate_writes_json_without_overwrite(tmp_path: Path):
    result = execution.write_research_applicability_campaign_execution_candidate_v1(tmp_path)

    assert (
        result["artifact_kind"]
        == execution.ARTIFACT_KIND_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_CANDIDATE
    )
    assert result["payload_sha256"]
    with pytest.raises(execution.ResearchApplicabilityCampaignExecutionCandidateError, match="already exists"):
        execution.write_research_applicability_campaign_execution_candidate_v1(tmp_path)


def test_research_applicability_campaign_execution_candidate_service_exports_are_public():
    import marketflow.services as services

    assert (
        services.ARTIFACT_KIND_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_CANDIDATE
        == "RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_CANDIDATE"
    )
    assert (
        services.RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_READY_FOR_OPERATOR_REVIEW
        == "RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_READY_FOR_OPERATOR_REVIEW"
    )
    assert services.build_research_applicability_campaign_execution_candidate_v1 is execution.build_research_applicability_campaign_execution_candidate_v1
    assert services.validate_research_applicability_campaign_execution_candidate_v1 is execution.validate_research_applicability_campaign_execution_candidate_v1
    assert services.write_research_applicability_campaign_execution_candidate_v1 is execution.write_research_applicability_campaign_execution_candidate_v1
    assert services.build_research_applicability_campaign_execution_candidate_markdown_v1 is execution.build_research_applicability_campaign_execution_candidate_markdown_v1
    assert services.research_applicability_campaign_execution_candidate_digest_v1 is execution.research_applicability_campaign_execution_candidate_digest_v1
