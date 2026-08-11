from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from marketflow import services
from marketflow.services import split_event_authority_candidate_service as split


def _candidate() -> dict[str, Any]:
    return split.build_split_event_authority_candidate_v1()


def _mutated_candidate(field: str, value: Any) -> dict[str, Any]:
    candidate = _candidate()
    candidate[field] = value
    return candidate


def test_candidate_builds_offline_without_provider_calls(monkeypatch: pytest.MonkeyPatch):
    def fail_provider_call(*_args: Any, **_kwargs: Any) -> None:  # pragma: no cover
        raise AssertionError("provider path must not be called")

    monkeypatch.setattr(
        split.approval.review.plan.approval_service.review_service.candidate_service.freeze_service.review_service.candidate_service.plan_review.plan.results_review.provider,
        "fetch_massive_ticker_details_v1",
        fail_provider_call,
    )

    candidate = _candidate()

    assert candidate["created_offline"] is True
    assert candidate["provider_requests_made"] is False
    assert candidate["live_validation_rerun_performed"] is False
    assert candidate["live_provider_transport_enabled"] is False


def test_artifact_kind_is_split_event_authority_candidate():
    assert _candidate()["artifact_kind"] == split.ARTIFACT_KIND_SPLIT_EVENT_AUTHORITY_CANDIDATE


def test_candidate_status_is_ready_for_operator_review():
    assert _candidate()["candidate_status"] == split.SPLIT_EVENT_AUTHORITY_READY_FOR_OPERATOR_REVIEW


def test_corporate_action_plan_approval_digest_is_bound():
    assert (
        _candidate()["corporate_action_authority_plan_approval_digest"]
        == split.EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST
    )


def test_corporate_action_plan_review_digest_is_bound():
    assert (
        _candidate()["corporate_action_authority_plan_candidate_review_package_digest"]
        == split.EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST
    )


def test_corporate_action_plan_candidate_digest_is_bound():
    assert (
        _candidate()["corporate_action_authority_plan_candidate_digest"]
        == split.EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_DIGEST
    )


def test_registry_inventory_approval_digest_is_bound():
    assert (
        _candidate()["post_identity_freeze_registry_inventory_approval_digest"]
        == split.approval.review.plan.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST
    )


def test_identity_freeze_digest_is_bound():
    assert (
        _candidate()["identity_authority_freeze_digest"]
        == split.approval.review.plan.approval_service.review_service.candidate_service.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST
    )


def test_live_validation_results_review_digest_is_bound():
    assert (
        _candidate()["live_ticker_validation_results_review_package_digest"]
        == split.approval.review.plan.approval_service.review_service.candidate_service.freeze_service.EXPECTED_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_DIGEST
    )


def test_target_universe_count_is_12():
    assert _candidate()["target_universe_count"] == 12


def test_target_universe_matches_corporate_action_plan_universe():
    candidate = _candidate()

    assert candidate["target_universe"] == split.VALIDATION_TARGET_UNIVERSE
    assert candidate["corporate_action_plan_universe"] == split.VALIDATION_TARGET_UNIVERSE


def test_identity_registry_plan_and_split_readiness_are_preserved():
    candidate = _candidate()

    assert candidate["identity_authority_frozen"] is True
    assert candidate["post_identity_freeze_registry_inventory_approved"] is True
    assert candidate["corporate_action_authority_plan_approved"] is True
    assert candidate["ready_for_split_event_authority_candidate"] is True


def test_split_event_candidate_objective_scope_creation_and_freeze_status():
    candidate = _candidate()

    assert candidate["split_event_authority_candidate_objective"] == (
        split.SPLIT_EVENT_AUTHORITY_CANDIDATE_OBJECTIVE
    )
    assert candidate["split_event_authority_candidate_scope"] == (
        split.SPLIT_EVENT_AUTHORITY_CANDIDATE_SCOPE
    )
    assert candidate["split_event_authority_creation_status"] == (
        split.SPLIT_EVENT_AUTHORITY_CREATION_STATUS
    )
    assert candidate["split_event_authority_freeze_status"] == (
        split.SPLIT_EVENT_AUTHORITY_FREEZE_STATUS
    )


def test_per_ticker_split_event_candidate_entries_are_candidate_only():
    entries = _candidate()["per_ticker_split_event_candidate_entries"]

    assert len(entries) == 12
    assert [entry["ticker"] for entry in entries] == split.VALIDATION_TARGET_UNIVERSE
    for entry in entries:
        assert entry["split_event_candidate_status"] == (
            split.SPLIT_EVENT_CANDIDATE_READY_FOR_OPERATOR_REVIEW
        )
        assert entry["split_event_authority_status"] == split.NOT_CREATED
        assert entry["split_event_freeze_status"] == split.NOT_FROZEN
        assert entry["provider_evidence_request_status"] == split.NOT_AUTHORIZED
        assert entry["provider_evidence_execution_status"] == split.NOT_EXECUTED
        assert entry["split_history_status"] == split.NOT_FETCHED
        assert entry["split_event_count_status"] == split.NOT_EVALUATED
        assert len(entry["per_ticker_split_event_candidate_digest"]) == 64
        assert entry["per_ticker_split_event_candidate_digest"] == (
            split.per_ticker_split_event_candidate_digest_v1(entry)
        )


def test_split_evidence_requirements_policy_chains_gates_and_risks_are_defined():
    candidate = _candidate()

    assert candidate["split_event_evidence_requirements"] == (
        split.SPLIT_EVENT_EVIDENCE_REQUIREMENTS
    )
    assert candidate["future_split_provider_request_policy"] == (
        split.FUTURE_SPLIT_PROVIDER_REQUEST_POLICY
    )
    assert candidate["future_split_authority_chain"] == split.FUTURE_SPLIT_AUTHORITY_CHAIN
    assert candidate["future_corporate_action_readiness_chain"] == (
        split.FUTURE_CORPORATE_ACTION_READINESS_CHAIN
    )
    assert candidate["future_gates"] == split.FUTURE_GATES
    assert candidate["risk_controls"] == split.RISK_CONTROLS


def test_planned_outputs_are_not_generated_and_research_only():
    candidate = _candidate()

    assert candidate["planned_output_count"] == len(split.PLANNED_OUTPUT_NAMES)
    assert {item["generation_status"] for item in candidate["planned_outputs"]} == {
        split.PLANNED_NOT_GENERATED
    }
    assert {item["generated"] for item in candidate["planned_outputs"]} == {False}
    assert {item["actionability"] for item in candidate["planned_outputs"]} == {
        split.RESEARCH_ONLY_NON_ACTIONABLE
    }


@pytest.mark.parametrize(
    "field",
    [
        "provider_requests_made",
        "live_validation_rerun_performed",
        "live_provider_transport_enabled",
        "split_event_authority_review_created",
        "split_event_authority_created",
        "split_event_authority_frozen",
        "split_provider_evidence_request_authorized",
        "split_provider_evidence_executed",
        "split_provider_evidence_results_created",
        "dividend_event_authority_candidate_created",
        "dividend_event_authority_created",
        "dividend_event_authority_frozen",
        "corporate_action_authority_created",
        "new_ticker_acquisition_authorized",
        "dataset_generation_authorized",
        "acquisition_generation_authorized",
        "canonical_dataset_authorized",
        "registry_approval_created",
        "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed",
        "predictive_experiment_rerun_authorized",
        "predictive_experiment_rerun_performed",
        "walk_forward_rerun_performed",
        "label_regeneration_performed",
        "feature_matrix_regeneration_performed",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
        "predictive_usefulness_acceptance_ready",
        "predictive_usefulness_acceptance_recommended",
        "predictive_usefulness_acceptance_candidate_created",
        "profitability_acceptance_ready",
        "profitability_acceptance_recommended",
        "runtime_migration_recommended",
        "runtime_migration_approved",
        "runtime_migration_active",
        "strategy_runtime_migration",
        "automatic_stitching",
    ],
)
def test_forbidden_boolean_fields_remain_false(field: str):
    assert _candidate()[field] is False


def test_runtime_strategy_paper_and_broker_remain_not_authorized():
    candidate = _candidate()

    assert candidate["runtime_use"] == split.NOT_AUTHORIZED
    assert candidate["strategy_use"] == split.NOT_AUTHORIZED
    assert candidate["paper_trading"] == split.NOT_AUTHORIZED
    assert candidate["broker_execution"] == split.NOT_AUTHORIZED


def test_ready_for_provider_request_and_freeze_remain_false():
    candidate = _candidate()

    assert candidate["ready_for_split_event_provider_evidence_request_approval"] is False
    assert candidate["ready_for_split_event_authority_freeze"] is False


def test_predictive_and_profitability_acceptance_remain_not_accepted():
    candidate = _candidate()

    assert candidate["predictive_usefulness"] == split.acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED
    assert candidate["profitability"] == split.acquisition.PROFITABILITY_NOT_ACCEPTED


def test_candidate_checklist_contains_all_required_check_ids():
    assert [item["check_id"] for item in _candidate()["candidate_checklist"]] == (
        split.REQUIRED_CHECK_IDS
    )


def test_all_checks_pass_for_valid_candidate():
    assert {item["status"] for item in _candidate()["candidate_checklist"]} == {split.PASS}


def test_summary_counts_total_passed_failed_correctly():
    summary = _candidate()["candidate_summary"]

    assert summary["total_checks"] == len(split.REQUIRED_CHECK_IDS)
    assert summary["passed_checks"] == len(split.REQUIRED_CHECK_IDS)
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["ready_for_operator_review"] is True
    assert summary["ready_for_split_event_provider_evidence_request_approval"] is False
    assert summary["ready_for_split_event_authority_freeze"] is False
    assert summary["split_event_authority_authorized"] is False
    assert summary["dividend_event_authority_authorized"] is False
    assert summary["corporate_action_authority_authorized"] is False
    assert summary["runtime_migration_authorized"] is False


def test_candidate_digest_is_deterministic():
    assert _candidate()["split_event_authority_candidate_digest"] == (
        _candidate()["split_event_authority_candidate_digest"]
    )


def test_per_ticker_split_event_candidate_digests_are_deterministic():
    first = _candidate()["per_ticker_split_event_candidate_entries"]
    second = _candidate()["per_ticker_split_event_candidate_entries"]

    assert [entry["per_ticker_split_event_candidate_digest"] for entry in first] == [
        entry["per_ticker_split_event_candidate_digest"] for entry in second
    ]


def test_validator_accepts_valid_candidate():
    validation = split.validate_split_event_authority_candidate_v1(_candidate())

    assert validation["status"] == "SPLIT_EVENT_AUTHORITY_CANDIDATE_VALID"
    assert validation["split_event_authority_candidate_created"] is True
    assert validation["split_event_authority_created"] is False


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "WRONG"),
        ("candidate_status", "WRONG"),
        ("provider_requests_made", True),
        ("live_validation_rerun_performed", True),
        ("live_provider_transport_enabled", True),
        ("target_universe_count", 11),
        ("identity_authority_frozen", False),
        ("post_identity_freeze_registry_inventory_approved", False),
        ("corporate_action_authority_plan_approved", False),
        ("ready_for_split_event_authority_candidate", False),
        ("split_event_authority_candidate_scope", "AUTHORITY"),
        ("split_event_authority_created", True),
        ("split_event_authority_frozen", True),
        ("split_provider_evidence_request_authorized", True),
        ("split_provider_evidence_executed", True),
        ("split_provider_evidence_results_created", True),
        ("dividend_event_authority_candidate_created", True),
        ("dividend_event_authority_created", True),
        ("dividend_event_authority_frozen", True),
        ("corporate_action_authority_created", True),
        ("new_ticker_acquisition_authorized", True),
        ("dataset_generation_authorized", True),
        ("acquisition_generation_authorized", True),
        ("canonical_dataset_authorized", True),
        ("registry_approval_created", True),
        ("additional_predictive_evidence_execution_authorized", True),
        ("additional_predictive_evidence_executed", True),
        ("predictive_experiment_rerun_authorized", True),
        ("predictive_experiment_rerun_performed", True),
        ("walk_forward_rerun_performed", True),
        ("label_regeneration_performed", True),
        ("feature_matrix_regeneration_performed", True),
        ("new_strategy_scoring_performed", True),
        ("trade_recommendations_generated", True),
        ("predictive_usefulness", "accepted"),
        ("predictive_usefulness_acceptance_ready", True),
        ("predictive_usefulness_acceptance_recommended", True),
        ("predictive_usefulness_acceptance_candidate_created", True),
        ("profitability", "accepted"),
        ("profitability_acceptance_ready", True),
        ("profitability_acceptance_recommended", True),
        ("runtime_migration_recommended", True),
        ("runtime_migration_approved", True),
        ("runtime_migration_active", True),
        ("strategy_runtime_migration", True),
        ("runtime_use", "AUTHORIZED"),
        ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
        ("automatic_stitching", True),
    ],
)
def test_validator_rejects_invalid_top_level_mutations(field: str, value: Any):
    with pytest.raises(split.SplitEventAuthorityCandidateError):
        split.validate_split_event_authority_candidate_v1(_mutated_candidate(field, value))


def test_validator_rejects_target_universe_mismatch():
    candidate = _candidate()
    candidate["target_universe"] = list(reversed(candidate["target_universe"]))

    with pytest.raises(split.SplitEventAuthorityCandidateError):
        split.validate_split_event_authority_candidate_v1(candidate)


def test_validator_rejects_per_ticker_candidate_count_not_12():
    candidate = _candidate()
    candidate["per_ticker_split_event_candidate_entries"] = (
        candidate["per_ticker_split_event_candidate_entries"][:11]
    )

    with pytest.raises(split.SplitEventAuthorityCandidateError):
        split.validate_split_event_authority_candidate_v1(candidate)


def test_validator_rejects_missing_per_ticker_candidate_digest():
    candidate = _candidate()
    candidate["per_ticker_split_event_candidate_entries"][0].pop(
        "per_ticker_split_event_candidate_digest"
    )

    with pytest.raises(split.SplitEventAuthorityCandidateError):
        split.validate_split_event_authority_candidate_v1(candidate)


@pytest.mark.parametrize(
    "field",
    [
        "split_event_evidence_requirements",
        "future_split_provider_request_policy",
        "future_split_authority_chain",
        "future_corporate_action_readiness_chain",
        "future_gates",
        "risk_controls",
    ],
)
def test_validator_rejects_missing_required_planning_sections(field: str):
    candidate = _candidate()
    candidate[field] = [] if isinstance(candidate[field], list) else {}

    with pytest.raises(split.SplitEventAuthorityCandidateError):
        split.validate_split_event_authority_candidate_v1(candidate)


def test_validator_rejects_missing_corporate_action_plan_approval_digest():
    candidate = _candidate()
    candidate.pop("corporate_action_authority_plan_approval_digest")

    with pytest.raises(split.SplitEventAuthorityCandidateError):
        split.validate_split_event_authority_candidate_v1(candidate)


def test_validator_rejects_missing_candidate_digest():
    candidate = _candidate()
    candidate.pop("split_event_authority_candidate_digest")

    with pytest.raises(split.SplitEventAuthorityCandidateError):
        split.validate_split_event_authority_candidate_v1(candidate)


def test_markdown_builder_includes_required_sections():
    markdown = split.build_split_event_authority_candidate_markdown_v1(_candidate())

    for section in [
        "## Title",
        "## Purpose",
        "## Source Corporate-Action Plan Approval",
        "## Target Universe",
        "## Split Event Authority Candidate Objective",
        "## Per-Ticker Split Event Candidate Entries",
        "## Split Event Evidence Requirements",
        "## Future Split Provider Request Policy",
        "## Future Split Authority Chain",
        "## Future Corporate-Action Readiness Chain",
        "## Future Gates",
        "## Risk Controls",
        "## Split Authority Boundary",
        "## Dividend Boundary",
        "## Corporate-Action Authority Boundary",
        "## Acquisition Boundary",
        "## Dataset Boundary",
        "## Predictive/Profitability Boundary",
        "## Runtime Boundary",
        "## Checklist Summary",
        "## Guardrails",
    ]:
        assert section in markdown


def test_writer_emits_json_and_refuses_overwrite(tmp_path: Path):
    result = split.write_split_event_authority_candidate_v1(tmp_path)
    payload = json.loads((tmp_path / result["filename"]).read_text(encoding="utf-8"))

    assert result["filename"] == "split_event_authority_candidate_v1.json"
    assert payload["artifact_kind"] == split.ARTIFACT_KIND_SPLIT_EVENT_AUTHORITY_CANDIDATE
    with pytest.raises(split.SplitEventAuthorityCandidateError):
        split.write_split_event_authority_candidate_v1(tmp_path)


def test_top_level_services_exports_are_available():
    candidate = _candidate()

    assert services.ARTIFACT_KIND_SPLIT_EVENT_AUTHORITY_CANDIDATE == (
        split.ARTIFACT_KIND_SPLIT_EVENT_AUTHORITY_CANDIDATE
    )
    assert services.SPLIT_EVENT_AUTHORITY_READY_FOR_OPERATOR_REVIEW == (
        split.SPLIT_EVENT_AUTHORITY_READY_FOR_OPERATOR_REVIEW
    )
    assert services.split_event_authority_candidate_digest_v1(candidate) == (
        candidate["split_event_authority_candidate_digest"]
    )
    assert services.validate_split_event_authority_candidate_v1(candidate)["status"] == (
        "SPLIT_EVENT_AUTHORITY_CANDIDATE_VALID"
    )
