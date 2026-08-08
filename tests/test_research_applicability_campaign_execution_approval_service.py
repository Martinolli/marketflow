from __future__ import annotations

from pathlib import Path

import pytest

from marketflow.services import research_applicability_campaign_execution_approval_service as approval


def _attestation(**overrides) -> dict:
    values = {
        "operator_reference": "TEST_OPERATOR",
        "operator_attestation_timestamp_utc": "2026-08-08T00:00:00Z",
        "operator_attestation_phrase": (
            approval.REQUIRED_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_APPROVAL_ATTESTATION_PHRASE
        ),
        "operator_confirms_execution_candidate_digest": approval.EXPECTED_EXECUTION_CANDIDATE_DIGEST,
        "operator_confirms_execution_candidate_review_package_digest": (
            approval.EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "operator_confirms_execution_request_id": (
            approval.candidate_review.execution_candidate.CAMPAIGN_EXECUTION_REQUEST_ID
        ),
        "operator_confirms_campaign_plan_digest": (
            approval.candidate_review.execution_candidate.EXPECTED_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_DIGEST
        ),
        "operator_confirms_campaign_plan_review_package_digest": (
            approval.candidate_review.execution_candidate.EXPECTED_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_REVIEW_PACKAGE_DIGEST
        ),
        "operator_confirms_dataset_availability_review_digest": (
            approval.candidate_review.execution_candidate.EXPECTED_DATASET_FILE_AVAILABILITY_VERIFICATION_REVIEW_PACKAGE_DIGEST
        ),
        "operator_confirms_swing_registry_approval_digest": (
            approval.candidate_review.execution_candidate.plan_review.campaign_plan.availability_review.verification.discovery.runtime_planning.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST
        ),
        "operator_confirms_position_swing_registry_approval_digest": (
            approval.candidate_review.execution_candidate.plan_review.campaign_plan.availability_review.verification.discovery.runtime_planning.EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST
        ),
        "operator_confirms_research_only_scope": True,
        "operator_confirms_aapl_only": True,
        "operator_confirms_profiles_swing_and_position_swing": True,
        "operator_confirms_no_provider_requests_in_approval": True,
        "operator_confirms_no_campaign_execution_performed": True,
        "operator_confirms_no_campaign_results_generated": True,
        "operator_confirms_no_runtime_migration_approval": True,
        "operator_confirms_no_runtime_activation": True,
        "operator_confirms_no_strategy_runtime_migration": True,
        "operator_confirms_no_paper_trading": True,
        "operator_confirms_no_broker_execution": True,
        "operator_confirms_no_predictive_usefulness": True,
        "operator_confirms_no_profitability_acceptance": True,
    }
    values.update(overrides)
    return approval.build_research_applicability_campaign_execution_approval_attestation_v1(**values)


def _approved() -> dict:
    return approval.build_research_applicability_campaign_execution_approved_v1(
        operator_attestation=_attestation()
    )


def test_operator_attestation_builder_creates_required_fields():
    attestation = _attestation()

    assert (
        attestation["operator_decision"]
        == approval.OPERATOR_DECISION_APPROVE_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION
    )
    assert (
        attestation["operator_attestation_phrase"]
        == approval.REQUIRED_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_APPROVAL_ATTESTATION_PHRASE
    )
    assert attestation["operator_reference"] == "TEST_OPERATOR"
    assert attestation["operator_confirms_execution_candidate_digest"] == approval.EXPECTED_EXECUTION_CANDIDATE_DIGEST
    assert (
        attestation["operator_confirms_execution_candidate_review_package_digest"]
        == approval.EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST
    )


def test_approved_artifact_builds_offline_without_provider_calls(monkeypatch: pytest.MonkeyPatch):
    def fail_provider_call(*_args, **_kwargs):  # pragma: no cover
        raise AssertionError("provider path must not be called")

    monkeypatch.setattr(approval.acquisition, "fetch_massive_custom_bars_v1", fail_provider_call)

    artifact = _approved()

    assert artifact["created_offline"] is True
    assert artifact["provider_requests_made_in_approval"] is False


def test_artifact_kind_is_execution_approved():
    assert (
        _approved()["artifact_kind"]
        == approval.ARTIFACT_KIND_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_APPROVED
    )


def test_approval_status_is_execution_approved():
    assert _approved()["approval_status"] == approval.RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_APPROVED


def test_campaign_execution_authorized_is_true():
    assert _approved()["campaign_execution_authorized"] is True


def test_campaign_execution_performed_remains_false():
    assert _approved()["campaign_execution_performed"] is False


def test_campaign_results_generated_remains_false():
    assert _approved()["campaign_results_generated"] is False


def test_runtime_migration_approved_remains_false():
    assert _approved()["runtime_migration_approved"] is False


def test_runtime_migration_active_remains_false():
    assert _approved()["runtime_migration_active"] is False


def test_strategy_runtime_migration_remains_false():
    assert _approved()["strategy_runtime_migration"] is False


def test_runtime_use_remains_not_authorized():
    assert _approved()["runtime_use"] == approval.candidate_review.execution_candidate.NOT_AUTHORIZED


def test_strategy_use_remains_not_authorized():
    assert _approved()["strategy_use"] == approval.candidate_review.execution_candidate.NOT_AUTHORIZED


def test_paper_trading_remains_not_authorized():
    assert _approved()["paper_trading"] == approval.candidate_review.execution_candidate.NOT_AUTHORIZED


def test_broker_execution_remains_not_authorized():
    assert _approved()["broker_execution"] == approval.candidate_review.execution_candidate.NOT_AUTHORIZED


def test_predictive_usefulness_and_profitability_remain_not_accepted():
    artifact = _approved()

    assert artifact["predictive_usefulness"] == approval.acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED
    assert artifact["profitability"] == approval.acquisition.PROFITABILITY_NOT_ACCEPTED


def test_execution_candidate_digest_matches_expected():
    assert _approved()["source_execution_candidate_digest"] == approval.EXPECTED_EXECUTION_CANDIDATE_DIGEST


def test_execution_candidate_review_package_digest_matches_expected():
    assert (
        _approved()["source_execution_candidate_review_package_digest"]
        == approval.EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST
    )


def test_execution_request_id_matches_expected():
    assert (
        _approved()["campaign_execution_request_id"]
        == approval.candidate_review.execution_candidate.CAMPAIGN_EXECUTION_REQUEST_ID
    )


def test_campaign_plan_digest_matches_expected():
    assert (
        _approved()["research_campaign_plan_digest"]
        == approval.candidate_review.execution_candidate.EXPECTED_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_DIGEST
    )


def test_campaign_plan_review_digest_matches_expected():
    assert (
        _approved()["research_campaign_plan_review_package_digest"]
        == approval.candidate_review.execution_candidate.EXPECTED_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_REVIEW_PACKAGE_DIGEST
    )


def test_dataset_availability_review_digest_matches_expected():
    assert (
        _approved()["dataset_file_availability_verification_review_package_digest"]
        == approval.candidate_review.execution_candidate.EXPECTED_DATASET_FILE_AVAILABILITY_VERIFICATION_REVIEW_PACKAGE_DIGEST
    )


def test_swing_registry_approval_digest_matches_expected():
    assert (
        _approved()["swing_registry_approval_digest"]
        == approval.candidate_review.execution_candidate.plan_review.campaign_plan.availability_review.verification.discovery.runtime_planning.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST
    )


def test_position_swing_registry_approval_digest_matches_expected():
    assert (
        _approved()["position_swing_registry_approval_digest"]
        == approval.candidate_review.execution_candidate.plan_review.campaign_plan.availability_review.verification.discovery.runtime_planning.EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST
    )


def test_campaign_request_scope_remains_research_only():
    artifact = _approved()

    assert artifact["campaign_scope"] == "RESEARCH_ONLY"
    assert artifact["ticker_universe"] == ["AAPL"]
    assert artifact["dataset_profiles"] == ["SWING", "POSITION_SWING"]
    assert artifact["date_range_start"] == "2022-01-01"
    assert artifact["date_range_end"] == "2025-12-31"
    assert artifact["execution_mode"] == approval.candidate_review.execution_candidate.READ_ONLY_OFFLINE_RESEARCH


def test_planned_outputs_remain_not_generated_and_non_actionable():
    artifact = _approved()

    assert artifact["planned_output_count"] == 12
    assert artifact["planned_outputs_status"] == approval.candidate_review.execution_candidate.PLANNED_NOT_GENERATED
    assert artifact["planned_outputs_label"] == approval.candidate_review.execution_candidate.RESEARCH_ONLY_NON_ACTIONABLE
    for output in artifact["planned_outputs"]:
        assert output["generated"] is False
        assert output["output_label"] == approval.candidate_review.execution_candidate.RESEARCH_ONLY_NON_ACTIONABLE


def test_approval_checklist_contains_all_required_check_ids():
    assert [item["check_id"] for item in _approved()["approval_checklist"]] == approval.REQUIRED_APPROVAL_CHECK_IDS


def test_all_approval_checks_pass():
    assert {item["status"] for item in _approved()["approval_checklist"]} == {approval.PASS}


def test_approval_summary_counts_total_passed_failed_correctly():
    summary = _approved()["approval_summary"]

    assert summary["total_checks"] == len(approval.REQUIRED_APPROVAL_CHECK_IDS)
    assert summary["passed_checks"] == len(approval.REQUIRED_APPROVAL_CHECK_IDS)
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["campaign_execution_authorized_by_operator"] is True
    assert summary["campaign_execution_performed"] is False
    assert summary["software_runtime_migration_authorized"] is False
    assert summary["software_runtime_activation_authorized"] is False
    assert summary["software_predictive_usefulness_authorized"] is False
    assert summary["software_profitability_authorized"] is False


def test_operator_attestation_phrase_must_match_exactly():
    with pytest.raises(approval.ResearchApplicabilityCampaignExecutionApprovalError, match="operator_attestation_phrase_matches"):
        approval.build_research_applicability_campaign_execution_approved_v1(
            operator_attestation=_attestation(operator_attestation_phrase="APPROVE")
        )


def test_wrong_operator_decision_is_rejected():
    with pytest.raises(approval.ResearchApplicabilityCampaignExecutionApprovalError, match="operator_decision_approved"):
        approval.build_research_applicability_campaign_execution_approved_v1(
            operator_attestation=_attestation(operator_decision="REJECT")
        )


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("operator_confirms_execution_candidate_digest", "0" * 64, "operator_execution_candidate_digest_confirmation_matches"),
        ("operator_confirms_execution_candidate_review_package_digest", "0" * 64, "operator_execution_candidate_review_digest_confirmation_matches"),
        ("operator_confirms_execution_request_id", "OTHER", "operator_execution_request_id_confirmation_matches"),
        ("operator_confirms_campaign_plan_digest", "0" * 64, "operator_campaign_plan_digest_confirmation_matches"),
        ("operator_confirms_campaign_plan_review_package_digest", "0" * 64, "operator_campaign_plan_review_digest_confirmation_matches"),
        ("operator_confirms_dataset_availability_review_digest", "0" * 64, "operator_dataset_availability_review_digest_confirmation_matches"),
        ("operator_confirms_swing_registry_approval_digest", "0" * 64, "operator_swing_registry_approval_digest_confirmation_matches"),
        ("operator_confirms_position_swing_registry_approval_digest", "0" * 64, "operator_position_swing_registry_approval_digest_confirmation_matches"),
        ("operator_confirms_research_only_scope", False, "operator_confirms_research_only_scope"),
        ("operator_confirms_aapl_only", False, "operator_confirms_aapl_only"),
        ("operator_confirms_profiles_swing_and_position_swing", False, "operator_confirms_profiles_swing_and_position_swing"),
        ("operator_confirms_no_provider_requests_in_approval", False, "operator_confirms_no_provider_requests_in_approval"),
        ("operator_confirms_no_campaign_execution_performed", False, "operator_confirms_no_campaign_execution_performed"),
        ("operator_confirms_no_campaign_results_generated", False, "operator_confirms_no_campaign_results_generated"),
        ("operator_confirms_no_runtime_migration_approval", False, "operator_confirms_no_runtime_migration_approval"),
        ("operator_confirms_no_runtime_activation", False, "operator_confirms_no_runtime_activation"),
        ("operator_confirms_no_strategy_runtime_migration", False, "operator_confirms_no_strategy_runtime_migration"),
        ("operator_confirms_no_paper_trading", False, "operator_confirms_no_paper_trading"),
        ("operator_confirms_no_broker_execution", False, "operator_confirms_no_broker_execution"),
        ("operator_confirms_no_predictive_usefulness", False, "operator_confirms_no_predictive_usefulness"),
        ("operator_confirms_no_profitability_acceptance", False, "operator_confirms_no_profitability_acceptance"),
    ],
)
def test_operator_attestation_rejects_bad_confirmations(field: str, value, match: str):
    with pytest.raises(approval.ResearchApplicabilityCampaignExecutionApprovalError, match=match):
        approval.build_research_applicability_campaign_execution_approved_v1(
            operator_attestation=_attestation(**{field: value})
        )


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("artifact_kind", "WRONG", "artifact_kind"),
        ("approval_status", "WRONG", "approval_status"),
        ("campaign_execution_authorized", False, "campaign_execution_authorized"),
        ("campaign_execution_performed", True, "campaign_execution_performed"),
        ("campaign_results_generated", True, "campaign_results_generated"),
        ("source_execution_candidate_digest", "0" * 64, "source_execution_candidate_digest"),
        ("source_execution_candidate_review_package_digest", "0" * 64, "source_execution_candidate_review_package_digest"),
        ("campaign_execution_request_id", "OTHER", "campaign_execution_request_id"),
        ("research_campaign_plan_digest", "0" * 64, "research_campaign_plan_digest"),
        ("dataset_file_availability_verification_review_package_digest", "0" * 64, "dataset_file_availability_verification_review_package_digest"),
        ("swing_registry_approval_digest", "0" * 64, "swing_registry_approval_digest"),
        ("position_swing_registry_approval_digest", "0" * 64, "position_swing_registry_approval_digest"),
        ("provider_requests_made_in_approval", True, "provider_requests_made_in_approval"),
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
    ],
)
def test_validator_rejects_invalid_approval_mutations(field: str, value, match: str):
    artifact = _approved()
    artifact[field] = value

    with pytest.raises(approval.ResearchApplicabilityCampaignExecutionApprovalError, match=match):
        approval.validate_research_applicability_campaign_execution_approved_v1(artifact)


def test_validator_rejects_missing_operator_attestation():
    artifact = _approved()
    artifact["operator_attestation"] = None

    with pytest.raises(approval.ResearchApplicabilityCampaignExecutionApprovalError, match="operator_attestation"):
        approval.validate_research_applicability_campaign_execution_approved_v1(artifact)


def test_validator_rejects_mutated_digest_field():
    artifact = _approved()
    artifact["research_applicability_campaign_execution_approval_digest"] = "0" * 64

    with pytest.raises(
        approval.ResearchApplicabilityCampaignExecutionApprovalError,
        match="research_applicability_campaign_execution_approval_digest",
    ):
        approval.validate_research_applicability_campaign_execution_approved_v1(artifact)


def test_approval_artifact_digest_is_deterministic():
    first = _approved()
    second = _approved()

    assert first["research_applicability_campaign_execution_approval_digest"] == second[
        "research_applicability_campaign_execution_approval_digest"
    ]
    assert (
        first["research_applicability_campaign_execution_approval_digest"]
        == approval.research_applicability_campaign_execution_approval_digest_v1(first)
    )


def test_remaining_roadmap_contains_required_future_work():
    roadmap = _approved()["remaining_roadmap"]

    assert "Research-only applicability campaign execution." in roadmap
    assert "Campaign result operator review." in roadmap
    assert "Predictive usefulness review." in roadmap
    assert "Profitability review." in roadmap
    assert "Separate runtime migration approval ceremony, if ever authorized." in roadmap


def test_markdown_writer_includes_required_sections_and_guardrails():
    markdown = approval.build_research_applicability_campaign_execution_approved_markdown_v1(_approved())

    for section in (
        "## Title",
        "## Approved Research Campaign Execution",
        "## Operator Attestation",
        "## Source Execution Candidate Review Package",
        "## Campaign Scope",
        "## Execution Boundary",
        "## Runtime Boundary",
        "## Approval Checklist Summary",
        "## Remaining Required Tasks",
        "## Guardrails",
    ):
        assert section in markdown
    assert "Campaign execution performed: `False`" in markdown


def test_write_approval_artifact_writes_json_without_overwrite(tmp_path: Path):
    result = approval.write_research_applicability_campaign_execution_approved_v1(
        tmp_path,
        operator_attestation=_attestation(),
    )

    assert (
        result["artifact_kind"]
        == approval.ARTIFACT_KIND_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_APPROVED
    )
    assert result["payload_sha256"]
    with pytest.raises(approval.ResearchApplicabilityCampaignExecutionApprovalError, match="already exists"):
        approval.write_research_applicability_campaign_execution_approved_v1(
            tmp_path,
            operator_attestation=_attestation(),
        )


def test_research_applicability_campaign_execution_approval_service_exports_are_public():
    import marketflow.services as services

    assert (
        services.ARTIFACT_KIND_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_APPROVED
        == "RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_APPROVED"
    )
    assert (
        services.RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_APPROVED
        == "RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_APPROVED"
    )
    assert (
        services.REQUIRED_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_APPROVAL_ATTESTATION_PHRASE
        == approval.REQUIRED_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_APPROVAL_ATTESTATION_PHRASE
    )
    assert services.build_research_applicability_campaign_execution_approval_attestation_v1 is approval.build_research_applicability_campaign_execution_approval_attestation_v1
    assert services.build_research_applicability_campaign_execution_approved_v1 is approval.build_research_applicability_campaign_execution_approved_v1
    assert services.validate_research_applicability_campaign_execution_approved_v1 is approval.validate_research_applicability_campaign_execution_approved_v1
    assert services.write_research_applicability_campaign_execution_approved_v1 is approval.write_research_applicability_campaign_execution_approved_v1
    assert services.build_research_applicability_campaign_execution_approved_markdown_v1 is approval.build_research_applicability_campaign_execution_approved_markdown_v1
    assert services.research_applicability_campaign_execution_approval_digest_v1 is approval.research_applicability_campaign_execution_approval_digest_v1
