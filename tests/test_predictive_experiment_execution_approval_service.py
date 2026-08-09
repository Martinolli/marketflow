from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from marketflow.services import predictive_experiment_execution_approval_service as approval


EXPECTED_APPROVAL_DIGEST = (
    "d1578a7858da3686d7322f4405e8c5f8075fdb32efa4f77bdae6af2242f4f4be"
)


def _attestation(**overrides: Any) -> dict[str, Any]:
    plan_service = approval.candidate_review.candidate_service.plan_review_service.plan_service
    values = {
        "operator_reference": "TEST_OPERATOR",
        "operator_attestation_timestamp_utc": "2026-08-09T00:00:00Z",
        "operator_attestation_phrase": (
            approval.REQUIRED_PREDICTIVE_EXPERIMENT_EXECUTION_APPROVAL_ATTESTATION_PHRASE
        ),
        "operator_confirms_execution_candidate_digest": approval.EXPECTED_EXECUTION_CANDIDATE_DIGEST,
        "operator_confirms_execution_candidate_review_package_digest": (
            approval.EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "operator_confirms_execution_request_id": (
            approval.candidate_review.candidate_service.PREDICTIVE_EXPERIMENT_EXECUTION_REQUEST_ID
        ),
        "operator_confirms_predictive_experiment_plan_digest": (
            approval.candidate_review.candidate_service.EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_DIGEST
        ),
        "operator_confirms_predictive_experiment_plan_review_package_digest": (
            approval.candidate_review.candidate_service.EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_REVIEW_PACKAGE_DIGEST
        ),
        "operator_confirms_predictive_usefulness_candidate_digest": (
            plan_service.EXPECTED_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_DIGEST
        ),
        "operator_confirms_predictive_usefulness_candidate_review_package_digest": (
            plan_service.EXPECTED_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "operator_confirms_campaign_results_review_digest": (
            plan_service.EXPECTED_CAMPAIGN_EXECUTION_RESULTS_REVIEW_PACKAGE_DIGEST
        ),
        "operator_confirms_campaign_execution_digest": (
            plan_service.EXPECTED_CAMPAIGN_EXECUTION_DIGEST
        ),
        "operator_confirms_swing_registry_approval_digest": (
            plan_service.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST
        ),
        "operator_confirms_position_swing_registry_approval_digest": (
            plan_service.EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST
        ),
        **{field: True for field in approval.OPERATOR_CONFIRMATION_FIELDS},
    }
    values.update(overrides)
    return approval.build_predictive_experiment_execution_approval_attestation_v1(
        **values
    )


def _approved() -> dict[str, Any]:
    return approval.build_predictive_experiment_execution_approved_v1(
        operator_attestation=_attestation()
    )


def test_operator_attestation_builder_creates_required_fields():
    attestation = _attestation()

    assert (
        attestation["operator_decision"]
        == approval.OPERATOR_DECISION_APPROVE_PREDICTIVE_EXPERIMENT_EXECUTION
    )
    assert (
        attestation["operator_attestation_phrase"]
        == approval.REQUIRED_PREDICTIVE_EXPERIMENT_EXECUTION_APPROVAL_ATTESTATION_PHRASE
    )
    assert attestation["operator_reference"] == "TEST_OPERATOR"
    assert (
        attestation["operator_confirms_execution_candidate_digest"]
        == approval.EXPECTED_EXECUTION_CANDIDATE_DIGEST
    )
    assert (
        attestation["operator_confirms_execution_candidate_review_package_digest"]
        == approval.EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST
    )
    assert all(attestation[field] is True for field in approval.OPERATOR_CONFIRMATION_FIELDS)


def test_approved_artifact_builds_offline_without_provider_calls(
    monkeypatch: pytest.MonkeyPatch,
):
    def fail_provider_call(*_args: Any, **_kwargs: Any):  # pragma: no cover
        raise AssertionError("provider path must not be called")

    monkeypatch.setattr(
        approval.candidate_review.candidate_service.plan_review_service.plan_service.acquisition,
        "fetch_massive_custom_bars_v1",
        fail_provider_call,
    )

    artifact = _approved()

    assert artifact["created_offline"] is True
    assert artifact["provider_requests_made_in_approval"] is False


def test_artifact_kind_and_status_are_execution_approved():
    artifact = _approved()

    assert artifact["artifact_kind"] == (
        approval.ARTIFACT_KIND_PREDICTIVE_EXPERIMENT_EXECUTION_APPROVED
    )
    assert artifact["approval_status"] == approval.PREDICTIVE_EXPERIMENT_EXECUTION_APPROVED


def test_predictive_experiment_execution_authorized_is_true():
    assert _approved()["predictive_experiment_execution_authorized"] is True


@pytest.mark.parametrize(
    "field",
    [
        "predictive_experiment_executed",
        "walk_forward_validation_performed",
        "out_of_sample_evaluation_performed",
        "label_generation_performed",
        "feature_matrix_generation_performed",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
        "predictive_usefulness_acceptance_ready",
        "profitability_acceptance_ready",
        "runtime_migration_recommended",
        "runtime_migration_approved",
        "runtime_migration_active",
        "strategy_runtime_migration",
        "automatic_stitching",
    ],
)
def test_execution_results_acceptance_and_runtime_flags_remain_false(field: str):
    assert _approved()[field] is False


@pytest.mark.parametrize(
    "field",
    ["runtime_use", "strategy_use", "paper_trading", "broker_execution"],
)
def test_runtime_strategy_paper_and_broker_use_remain_not_authorized(field: str):
    assert (
        _approved()[field]
        == approval.candidate_review.candidate_service.NOT_AUTHORIZED
    )


def test_predictive_usefulness_and_profitability_remain_not_accepted():
    acquisition = (
        approval.candidate_review.candidate_service.plan_review_service.plan_service.acquisition
    )
    artifact = _approved()

    assert artifact["predictive_usefulness"] == acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED
    assert artifact["profitability"] == acquisition.PROFITABILITY_NOT_ACCEPTED


def test_source_execution_candidate_review_evidence_is_bound():
    artifact = _approved()
    candidate_service = approval.candidate_review.candidate_service
    plan_service = candidate_service.plan_review_service.plan_service

    assert artifact["source_execution_candidate_digest"] == (
        approval.EXPECTED_EXECUTION_CANDIDATE_DIGEST
    )
    assert artifact["source_execution_candidate_review_package_digest"] == (
        approval.EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST
    )
    assert artifact["predictive_experiment_execution_request_id"] == (
        candidate_service.PREDICTIVE_EXPERIMENT_EXECUTION_REQUEST_ID
    )
    assert artifact["predictive_experiment_plan_digest"] == (
        candidate_service.EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_DIGEST
    )
    assert artifact["predictive_experiment_plan_review_package_digest"] == (
        candidate_service.EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_REVIEW_PACKAGE_DIGEST
    )
    assert artifact["predictive_usefulness_review_candidate_digest"] == (
        plan_service.EXPECTED_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_DIGEST
    )
    assert artifact["predictive_usefulness_review_candidate_review_package_digest"] == (
        plan_service.EXPECTED_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_REVIEW_PACKAGE_DIGEST
    )
    assert artifact["campaign_results_review_package_digest"] == (
        plan_service.EXPECTED_CAMPAIGN_EXECUTION_RESULTS_REVIEW_PACKAGE_DIGEST
    )
    assert artifact["campaign_execution_digest"] == (
        plan_service.EXPECTED_CAMPAIGN_EXECUTION_DIGEST
    )
    assert artifact["swing_registry_approval_digest"] == (
        plan_service.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST
    )
    assert artifact["position_swing_registry_approval_digest"] == (
        plan_service.EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST
    )


def test_experiment_request_scope_remains_research_only():
    artifact = _approved()

    assert artifact["experiment_scope"] == "RESEARCH_ONLY"
    assert artifact["ticker_universe"] == ["AAPL"]
    assert [item["profile"] for item in artifact["dataset_profiles"]] == [
        "SWING",
        "POSITION_SWING",
    ]
    assert artifact["date_range_start"] == "2022-01-01"
    assert artifact["date_range_end"] == "2025-12-31"
    assert artifact["execution_mode"] == "OFFLINE_RESEARCH_EXPERIMENT"
    assert artifact["runtime_mode"] == "NOT_RUNTIME"
    assert artifact["strategy_mode"] == "NOT_STRATEGY_INPUT"
    assert artifact["broker_mode"] == "DISABLED"
    assert artifact["paper_trading_mode"] == "DISABLED"


def test_planned_outputs_remain_not_generated_and_non_actionable():
    artifact = _approved()

    assert artifact["planned_output_count"] == 13
    assert (
        artifact["planned_outputs_status"]
        == approval.candidate_review.candidate_service.PLANNED_NOT_GENERATED
    )
    assert (
        artifact["planned_outputs_label"]
        == approval.candidate_review.candidate_service.RESEARCH_ONLY_NON_ACTIONABLE
    )
    assert {item["generation_status"] for item in artifact["planned_outputs"]} == {
        approval.candidate_review.candidate_service.PLANNED_NOT_GENERATED
    }
    assert {item["output_label"] for item in artifact["planned_outputs"]} == {
        approval.candidate_review.candidate_service.RESEARCH_ONLY_NON_ACTIONABLE
    }


def test_approval_checklist_contains_all_required_check_ids_and_passes():
    checklist = _approved()["approval_checklist"]

    assert [item["check_id"] for item in checklist] == approval.REQUIRED_APPROVAL_CHECK_IDS
    assert {item["status"] for item in checklist} == {approval.PASS}


def test_approval_summary_counts_total_passed_failed_and_boundaries():
    summary = _approved()["approval_summary"]

    assert summary["total_checks"] == len(approval.REQUIRED_APPROVAL_CHECK_IDS)
    assert summary["passed_checks"] == len(approval.REQUIRED_APPROVAL_CHECK_IDS)
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["predictive_experiment_execution_authorized_by_operator"] is True
    assert summary["predictive_experiment_executed"] is False
    assert summary["software_predictive_usefulness_authorized"] is False
    assert summary["software_profitability_authorized"] is False
    assert summary["software_runtime_migration_authorized"] is False
    assert summary["software_runtime_activation_authorized"] is False


def test_operator_attestation_phrase_must_match_exactly():
    with pytest.raises(
        approval.PredictiveExperimentExecutionApprovalError,
        match="operator_attestation_phrase_matches",
    ):
        approval.build_predictive_experiment_execution_approved_v1(
            operator_attestation=_attestation(operator_attestation_phrase="APPROVE")
        )


def test_wrong_operator_decision_is_rejected():
    with pytest.raises(
        approval.PredictiveExperimentExecutionApprovalError,
        match="operator_decision_approved",
    ):
        approval.build_predictive_experiment_execution_approved_v1(
            operator_attestation=_attestation(operator_decision="REJECT")
        )


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        (
            "operator_confirms_execution_candidate_digest",
            "0" * 64,
            "operator_execution_candidate_digest_confirmation_matches",
        ),
        (
            "operator_confirms_execution_candidate_review_package_digest",
            "0" * 64,
            "operator_execution_candidate_review_digest_confirmation_matches",
        ),
        (
            "operator_confirms_execution_request_id",
            "OTHER",
            "operator_execution_request_id_confirmation_matches",
        ),
        (
            "operator_confirms_predictive_experiment_plan_digest",
            "0" * 64,
            "operator_predictive_experiment_plan_digest_confirmation_matches",
        ),
        (
            "operator_confirms_predictive_experiment_plan_review_package_digest",
            "0" * 64,
            "operator_predictive_experiment_plan_review_digest_confirmation_matches",
        ),
        (
            "operator_confirms_predictive_usefulness_candidate_digest",
            "0" * 64,
            "operator_predictive_usefulness_candidate_digest_confirmation_matches",
        ),
        (
            "operator_confirms_predictive_usefulness_candidate_review_package_digest",
            "0" * 64,
            "operator_predictive_usefulness_candidate_review_digest_confirmation_matches",
        ),
        (
            "operator_confirms_campaign_results_review_digest",
            "0" * 64,
            "operator_campaign_results_review_digest_confirmation_matches",
        ),
        (
            "operator_confirms_campaign_execution_digest",
            "0" * 64,
            "operator_campaign_execution_digest_confirmation_matches",
        ),
        (
            "operator_confirms_swing_registry_approval_digest",
            "0" * 64,
            "operator_swing_registry_approval_digest_confirmation_matches",
        ),
        (
            "operator_confirms_position_swing_registry_approval_digest",
            "0" * 64,
            "operator_position_swing_registry_approval_digest_confirmation_matches",
        ),
        *[(field, False, field) for field in approval.OPERATOR_CONFIRMATION_FIELDS],
    ],
)
def test_operator_attestation_rejects_bad_confirmations(
    field: str,
    value: Any,
    match: str,
):
    with pytest.raises(approval.PredictiveExperimentExecutionApprovalError, match=match):
        approval.build_predictive_experiment_execution_approved_v1(
            operator_attestation=_attestation(**{field: value})
        )


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("artifact_kind", "WRONG", "artifact_kind"),
        ("approval_status", "WRONG", "approval_status"),
        (
            "predictive_experiment_execution_authorized",
            False,
            "predictive_experiment_execution_authorized",
        ),
        ("predictive_experiment_executed", True, "predictive_experiment_executed"),
        ("walk_forward_validation_performed", True, "walk_forward_validation_performed"),
        (
            "out_of_sample_evaluation_performed",
            True,
            "out_of_sample_evaluation_performed",
        ),
        ("label_generation_performed", True, "label_generation_performed"),
        ("feature_matrix_generation_performed", True, "feature_matrix_generation_performed"),
        ("new_strategy_scoring_performed", True, "new_strategy_scoring_performed"),
        ("trade_recommendations_generated", True, "trade_recommendations_generated"),
        ("source_execution_candidate_digest", "0" * 64, "source_execution_candidate_digest"),
        (
            "source_execution_candidate_review_package_digest",
            "0" * 64,
            "source_execution_candidate_review_package_digest",
        ),
        (
            "predictive_experiment_execution_request_id",
            "OTHER",
            "predictive_experiment_execution_request_id",
        ),
        ("predictive_experiment_plan_digest", "0" * 64, "predictive_experiment_plan_digest"),
        (
            "predictive_experiment_plan_review_package_digest",
            "0" * 64,
            "predictive_experiment_plan_review_package_digest",
        ),
        ("provider_requests_made_in_approval", True, "provider_requests_made_in_approval"),
        ("runtime_migration_recommended", True, "runtime_migration_recommended"),
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
def test_validator_rejects_invalid_approval_mutations(
    field: str,
    value: Any,
    match: str,
):
    artifact = _approved()
    artifact[field] = value

    with pytest.raises(approval.PredictiveExperimentExecutionApprovalError, match=match):
        approval.validate_predictive_experiment_execution_approved_v1(artifact)


def test_validator_rejects_missing_operator_attestation():
    artifact = _approved()
    artifact["operator_attestation"] = None

    with pytest.raises(
        approval.PredictiveExperimentExecutionApprovalError,
        match="operator_decision_approved",
    ):
        approval.validate_predictive_experiment_execution_approved_v1(artifact)


def test_validator_rejects_mutated_digest_field():
    artifact = _approved()
    artifact["predictive_experiment_execution_approval_digest"] = "0" * 64

    with pytest.raises(
        approval.PredictiveExperimentExecutionApprovalError,
        match="predictive_experiment_execution_approval_digest",
    ):
        approval.validate_predictive_experiment_execution_approved_v1(artifact)


def test_approval_artifact_digest_is_deterministic():
    first = _approved()
    second = _approved()

    assert first["predictive_experiment_execution_approval_digest"] == second[
        "predictive_experiment_execution_approval_digest"
    ]
    assert first["predictive_experiment_execution_approval_digest"] == EXPECTED_APPROVAL_DIGEST
    assert first["predictive_experiment_execution_approval_digest"] == (
        approval.predictive_experiment_execution_approval_digest_v1(first)
    )


def test_remaining_roadmap_contains_required_future_work():
    roadmap = _approved()["remaining_roadmap"]

    assert "Predictive experiment execution." in roadmap
    assert "Predictive experiment results review." in roadmap
    assert "Predictive usefulness review." in roadmap
    assert "Profitability review." in roadmap
    assert "Separate runtime migration approval ceremony, if ever authorized." in roadmap


def test_markdown_writer_includes_required_sections_and_guardrails():
    markdown = approval.build_predictive_experiment_execution_approved_markdown_v1(
        _approved()
    )

    for section in (
        "## Title",
        "## Approved Predictive Experiment Execution",
        "## Operator Attestation",
        "## Source Execution Candidate Review Package",
        "## Experiment Scope",
        "## Execution Boundary",
        "## Predictive/Profitability Boundary",
        "## Runtime Boundary",
        "## Approval Checklist Summary",
        "## Remaining Required Tasks",
        "## Guardrails",
    ):
        assert section in markdown
    assert "Execution performed: `False`" in markdown
    assert "Runtime, Strategy, paper trading, and broker execution remain `NOT_AUTHORIZED`." in markdown


def test_write_approval_artifact_writes_json_without_overwrite(tmp_path: Path):
    result = approval.write_predictive_experiment_execution_approved_v1(
        tmp_path,
        operator_attestation=_attestation(),
    )

    assert result["artifact_kind"] == (
        approval.ARTIFACT_KIND_PREDICTIVE_EXPERIMENT_EXECUTION_APPROVED
    )
    assert result["payload_sha256"]
    with pytest.raises(
        approval.PredictiveExperimentExecutionApprovalError,
        match="already exists",
    ):
        approval.write_predictive_experiment_execution_approved_v1(
            tmp_path,
            operator_attestation=_attestation(),
        )


def test_predictive_experiment_execution_approval_service_exports_are_public():
    import marketflow.services as services

    assert services.ARTIFACT_KIND_PREDICTIVE_EXPERIMENT_EXECUTION_APPROVED == (
        approval.ARTIFACT_KIND_PREDICTIVE_EXPERIMENT_EXECUTION_APPROVED
    )
    assert services.PREDICTIVE_EXPERIMENT_EXECUTION_APPROVED == (
        approval.PREDICTIVE_EXPERIMENT_EXECUTION_APPROVED
    )
    assert (
        services.REQUIRED_PREDICTIVE_EXPERIMENT_EXECUTION_APPROVAL_ATTESTATION_PHRASE
        == approval.REQUIRED_PREDICTIVE_EXPERIMENT_EXECUTION_APPROVAL_ATTESTATION_PHRASE
    )
    assert services.build_predictive_experiment_execution_approval_attestation_v1 is (
        approval.build_predictive_experiment_execution_approval_attestation_v1
    )
    assert services.build_predictive_experiment_execution_approved_v1 is (
        approval.build_predictive_experiment_execution_approved_v1
    )
    assert services.validate_predictive_experiment_execution_approved_v1 is (
        approval.validate_predictive_experiment_execution_approved_v1
    )
    assert services.write_predictive_experiment_execution_approved_v1 is (
        approval.write_predictive_experiment_execution_approved_v1
    )
    assert services.build_predictive_experiment_execution_approved_markdown_v1 is (
        approval.build_predictive_experiment_execution_approved_markdown_v1
    )
    assert services.predictive_experiment_execution_approval_digest_v1 is (
        approval.predictive_experiment_execution_approval_digest_v1
    )
