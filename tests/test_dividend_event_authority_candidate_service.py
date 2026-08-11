from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from marketflow import services
from marketflow.services import dividend_event_authority_candidate_service as dividend


EXPECTED_CANDIDATE_DIGEST = (
    "44cabaebea32b4d618d13c4e1c77190c2549b9c15c8481460ab66211d1f44097"
)


def _candidate() -> dict[str, Any]:
    return dividend.build_dividend_event_authority_candidate_v1()


def _mutated_candidate(field: str, value: Any) -> dict[str, Any]:
    candidate = _candidate()
    candidate[field] = value
    return candidate


def test_candidate_builds_offline_without_provider_calls(monkeypatch: pytest.MonkeyPatch):
    def fail_provider_call(*_args: Any, **_kwargs: Any) -> None:  # pragma: no cover
        raise AssertionError("provider path must not be called")

    monkeypatch.setattr(
        dividend.split_review.candidate_service.approval.review.plan.approval_service.review_service.candidate_service.freeze_service.review_service.candidate_service.plan_review.plan.results_review.provider,
        "fetch_massive_ticker_details_v1",
        fail_provider_call,
    )

    candidate = _candidate()

    assert candidate["created_offline"] is True
    assert candidate["provider_requests_made"] is False
    assert candidate["live_validation_rerun_performed"] is False
    assert candidate["live_provider_transport_enabled"] is False


def test_artifact_kind_is_dividend_event_authority_candidate():
    assert _candidate()["artifact_kind"] == (
        dividend.ARTIFACT_KIND_DIVIDEND_EVENT_AUTHORITY_CANDIDATE
    )


def test_candidate_status_is_ready_for_operator_review():
    assert _candidate()["candidate_status"] == (
        dividend.DIVIDEND_EVENT_AUTHORITY_READY_FOR_OPERATOR_REVIEW
    )


def test_corporate_action_plan_approval_digest_is_bound():
    assert _candidate()["corporate_action_authority_plan_approval_digest"] == (
        dividend.EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST
    )


def test_corporate_action_plan_review_digest_is_bound():
    assert _candidate()["corporate_action_authority_plan_candidate_review_package_digest"] == (
        dividend.EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST
    )


def test_corporate_action_plan_candidate_digest_is_bound():
    assert _candidate()["corporate_action_authority_plan_candidate_digest"] == (
        dividend.EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_DIGEST
    )


def test_split_event_candidate_review_digest_is_bound():
    assert _candidate()["split_event_authority_candidate_review_package_digest"] == (
        dividend.EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST
    )


def test_split_event_candidate_digest_is_bound():
    assert _candidate()["split_event_authority_candidate_digest"] == (
        dividend.EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_DIGEST
    )


def test_registry_inventory_approval_digest_is_bound():
    assert _candidate()["post_identity_freeze_registry_inventory_approval_digest"] == (
        dividend.split_review.candidate_service.approval.review.plan.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST
    )


def test_identity_freeze_digest_is_bound():
    assert _candidate()["identity_authority_freeze_digest"] == (
        dividend.split_review.candidate_service.approval.review.plan.approval_service.review_service.candidate_service.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST
    )


def test_live_validation_results_review_digest_is_bound():
    assert _candidate()["live_ticker_validation_results_review_package_digest"] == (
        dividend.split_review.candidate_service.approval.review.plan.approval_service.review_service.candidate_service.freeze_service.EXPECTED_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_DIGEST
    )


def test_target_universe_count_is_12():
    assert _candidate()["target_universe_count"] == 12


def test_target_universe_matches_corporate_action_plan_universe():
    candidate = _candidate()

    assert candidate["target_universe"] == dividend.VALIDATION_TARGET_UNIVERSE
    assert candidate["corporate_action_plan_universe"] == (
        dividend.VALIDATION_TARGET_UNIVERSE
    )


def test_identity_registry_plan_and_dividend_readiness_are_preserved():
    candidate = _candidate()

    assert candidate["identity_authority_frozen"] is True
    assert candidate["post_identity_freeze_registry_inventory_approved"] is True
    assert candidate["corporate_action_authority_plan_approved"] is True
    assert candidate["ready_for_dividend_event_authority_candidate"] is True


def test_dividend_event_candidate_objective_scope_creation_and_freeze_status():
    candidate = _candidate()

    assert candidate["dividend_event_authority_candidate_objective"] == (
        dividend.DIVIDEND_EVENT_AUTHORITY_CANDIDATE_OBJECTIVE
    )
    assert candidate["dividend_event_authority_candidate_scope"] == (
        dividend.DIVIDEND_EVENT_AUTHORITY_CANDIDATE_SCOPE
    )
    assert candidate["dividend_event_authority_creation_status"] == (
        dividend.DIVIDEND_EVENT_AUTHORITY_CREATION_STATUS
    )
    assert candidate["dividend_event_authority_freeze_status"] == (
        dividend.DIVIDEND_EVENT_AUTHORITY_FREEZE_STATUS
    )


def test_per_ticker_dividend_event_candidate_entries_are_candidate_only():
    entries = _candidate()["per_ticker_dividend_event_candidate_entries"]

    assert len(entries) == 12
    assert [entry["ticker"] for entry in entries] == dividend.VALIDATION_TARGET_UNIVERSE
    for entry in entries:
        assert entry["dividend_event_candidate_status"] == (
            dividend.DIVIDEND_EVENT_CANDIDATE_READY_FOR_OPERATOR_REVIEW
        )
        assert entry["dividend_event_authority_status"] == dividend.NOT_CREATED
        assert entry["dividend_event_freeze_status"] == dividend.NOT_FROZEN
        assert entry["provider_evidence_request_status"] == dividend.NOT_AUTHORIZED
        assert entry["provider_evidence_execution_status"] == dividend.NOT_EXECUTED
        assert entry["dividend_history_status"] == dividend.NOT_FETCHED
        assert entry["dividend_event_count_status"] == dividend.NOT_EVALUATED
        assert len(entry["source_identity_freeze_digest"]) == 64
        assert len(entry["source_registry_inventory_approval_digest"]) == 64
        assert len(entry["source_corporate_action_plan_approval_digest"]) == 64
        assert len(entry["source_split_event_candidate_review_digest"]) == 64
        assert len(entry["per_ticker_dividend_event_candidate_digest"]) == 64
        assert entry["per_ticker_dividend_event_candidate_digest"] == (
            dividend.per_ticker_dividend_event_candidate_digest_v1(entry)
        )


def test_dividend_evidence_policy_chains_gates_and_risks_are_defined():
    candidate = _candidate()

    assert candidate["dividend_event_evidence_requirements"] == (
        dividend.DIVIDEND_EVENT_EVIDENCE_REQUIREMENTS
    )
    assert candidate["dividend_policy_reconciliation_requirements"] == (
        dividend.DIVIDEND_POLICY_RECONCILIATION_REQUIREMENTS
    )
    assert candidate["future_dividend_provider_request_policy"] == (
        dividend.FUTURE_DIVIDEND_PROVIDER_REQUEST_POLICY
    )
    assert candidate["future_dividend_authority_chain"] == (
        dividend.FUTURE_DIVIDEND_AUTHORITY_CHAIN
    )
    assert candidate["future_corporate_action_readiness_chain"] == (
        dividend.FUTURE_CORPORATE_ACTION_READINESS_CHAIN
    )
    assert candidate["future_gates"] == dividend.FUTURE_GATES
    assert candidate["risk_controls"] == dividend.RISK_CONTROLS


def test_planned_outputs_are_not_generated_and_research_only():
    candidate = _candidate()

    assert candidate["planned_output_count"] == len(dividend.PLANNED_OUTPUT_NAMES)
    assert {item["generation_status"] for item in candidate["planned_outputs"]} == {
        dividend.PLANNED_NOT_GENERATED
    }
    assert {item["generated"] for item in candidate["planned_outputs"]} == {False}
    assert {item["actionability"] for item in candidate["planned_outputs"]} == {
        dividend.RESEARCH_ONLY_NON_ACTIONABLE
    }


@pytest.mark.parametrize(
    "field",
    [
        "provider_requests_made",
        "live_validation_rerun_performed",
        "live_provider_transport_enabled",
        "dividend_event_authority_review_created",
        "dividend_event_authority_created",
        "dividend_event_authority_frozen",
        "dividend_provider_evidence_request_authorized",
        "dividend_provider_evidence_executed",
        "dividend_provider_evidence_results_created",
        "split_event_authority_created",
        "split_event_authority_frozen",
        "split_provider_evidence_request_authorized",
        "split_provider_evidence_executed",
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


def test_dividend_candidate_created_is_only_candidate_artifact_transition():
    candidate = _candidate()

    assert candidate["dividend_event_authority_candidate_created"] is True
    assert candidate["dividend_event_authority_review_created"] is False
    assert candidate["dividend_event_authority_created"] is False
    assert candidate["dividend_event_authority_frozen"] is False


def test_split_candidate_review_is_source_but_split_authority_remains_closed():
    candidate = _candidate()

    assert candidate["split_event_authority_candidate_created"] is True
    assert candidate["split_event_authority_review_created"] is True
    assert candidate["split_event_authority_created"] is False
    assert candidate["split_event_authority_frozen"] is False
    assert candidate["split_provider_evidence_request_authorized"] is False
    assert candidate["split_provider_evidence_executed"] is False


def test_runtime_strategy_paper_and_broker_remain_not_authorized():
    candidate = _candidate()

    assert candidate["runtime_use"] == dividend.NOT_AUTHORIZED
    assert candidate["strategy_use"] == dividend.NOT_AUTHORIZED
    assert candidate["paper_trading"] == dividend.NOT_AUTHORIZED
    assert candidate["broker_execution"] == dividend.NOT_AUTHORIZED


def test_ready_for_provider_request_and_freeze_remain_false():
    candidate = _candidate()

    assert candidate["ready_for_dividend_provider_evidence_request_approval"] is False
    assert candidate["ready_for_dividend_event_authority_freeze"] is False


def test_predictive_and_profitability_acceptance_remain_not_accepted():
    candidate = _candidate()

    assert candidate["predictive_usefulness"] == (
        dividend.acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED
    )
    assert candidate["profitability"] == dividend.acquisition.PROFITABILITY_NOT_ACCEPTED


def test_candidate_checklist_contains_all_required_check_ids():
    assert [item["check_id"] for item in _candidate()["candidate_checklist"]] == (
        dividend.REQUIRED_CHECK_IDS
    )


def test_all_checks_pass_for_valid_candidate():
    assert {item["status"] for item in _candidate()["candidate_checklist"]} == {
        dividend.PASS
    }


def test_summary_counts_total_passed_failed_correctly():
    summary = _candidate()["candidate_summary"]

    assert summary == {
        "total_checks": len(dividend.REQUIRED_CHECK_IDS),
        "passed_checks": len(dividend.REQUIRED_CHECK_IDS),
        "failed_checks": 0,
        "blocker_count": 0,
        "ready_for_operator_review": True,
        "ready_for_dividend_provider_evidence_request_approval": False,
        "ready_for_dividend_event_authority_freeze": False,
        "dividend_event_authority_authorized": False,
        "dividend_event_authority_frozen": False,
        "split_event_authority_authorized": False,
        "corporate_action_authority_authorized": False,
        "acquisition_authorized": False,
        "dataset_generation_authorized": False,
        "additional_predictive_evidence_execution_authorized": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def test_candidate_digest_is_deterministic():
    assert _candidate()["dividend_event_authority_candidate_digest"] == (
        _candidate()["dividend_event_authority_candidate_digest"]
    )
    assert _candidate()["dividend_event_authority_candidate_digest"] == (
        EXPECTED_CANDIDATE_DIGEST
    )


def test_per_ticker_dividend_event_candidate_digests_are_deterministic():
    first = _candidate()["per_ticker_dividend_event_candidate_entries"]
    second = _candidate()["per_ticker_dividend_event_candidate_entries"]

    assert [entry["per_ticker_dividend_event_candidate_digest"] for entry in first] == [
        entry["per_ticker_dividend_event_candidate_digest"] for entry in second
    ]


def test_validator_accepts_valid_candidate():
    validation = dividend.validate_dividend_event_authority_candidate_v1(_candidate())

    assert validation["status"] == "DIVIDEND_EVENT_AUTHORITY_CANDIDATE_VALID"
    assert validation["dividend_event_authority_candidate_created"] is True
    assert validation["dividend_event_authority_created"] is False
    assert validation["dividend_event_authority_frozen"] is False


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
        ("ready_for_dividend_event_authority_candidate", False),
        ("dividend_event_authority_candidate_scope", "AUTHORITY"),
        ("dividend_event_authority_created", True),
        ("dividend_event_authority_frozen", True),
        ("dividend_provider_evidence_request_authorized", True),
        ("dividend_provider_evidence_executed", True),
        ("dividend_provider_evidence_results_created", True),
        ("split_event_authority_created", True),
        ("split_event_authority_frozen", True),
        ("split_provider_evidence_request_authorized", True),
        ("split_provider_evidence_executed", True),
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
    with pytest.raises(dividend.DividendEventAuthorityCandidateError):
        dividend.validate_dividend_event_authority_candidate_v1(
            _mutated_candidate(field, value)
        )


def test_validator_rejects_target_universe_mismatch():
    candidate = _candidate()
    candidate["target_universe"] = list(reversed(candidate["target_universe"]))

    with pytest.raises(dividend.DividendEventAuthorityCandidateError):
        dividend.validate_dividend_event_authority_candidate_v1(candidate)


def test_validator_rejects_per_ticker_candidate_count_not_12():
    candidate = _candidate()
    candidate["per_ticker_dividend_event_candidate_entries"] = (
        candidate["per_ticker_dividend_event_candidate_entries"][:11]
    )

    with pytest.raises(dividend.DividendEventAuthorityCandidateError):
        dividend.validate_dividend_event_authority_candidate_v1(candidate)


def test_validator_rejects_missing_per_ticker_candidate_digest():
    candidate = _candidate()
    candidate["per_ticker_dividend_event_candidate_entries"][0].pop(
        "per_ticker_dividend_event_candidate_digest"
    )

    with pytest.raises(dividend.DividendEventAuthorityCandidateError):
        dividend.validate_dividend_event_authority_candidate_v1(candidate)


@pytest.mark.parametrize(
    "field",
    [
        "dividend_event_evidence_requirements",
        "dividend_policy_reconciliation_requirements",
        "future_dividend_provider_request_policy",
        "future_dividend_authority_chain",
        "future_corporate_action_readiness_chain",
        "future_gates",
        "risk_controls",
    ],
)
def test_validator_rejects_missing_required_planning_sections(field: str):
    candidate = _candidate()
    candidate[field] = [] if isinstance(candidate[field], list) else {}

    with pytest.raises(dividend.DividendEventAuthorityCandidateError):
        dividend.validate_dividend_event_authority_candidate_v1(candidate)


def test_validator_rejects_missing_corporate_action_plan_approval_digest():
    candidate = _candidate()
    candidate.pop("corporate_action_authority_plan_approval_digest")

    with pytest.raises(dividend.DividendEventAuthorityCandidateError):
        dividend.validate_dividend_event_authority_candidate_v1(candidate)


def test_validator_rejects_missing_candidate_digest():
    candidate = _candidate()
    candidate.pop("dividend_event_authority_candidate_digest")

    with pytest.raises(dividend.DividendEventAuthorityCandidateError):
        dividend.validate_dividend_event_authority_candidate_v1(candidate)


def test_markdown_builder_includes_required_sections():
    markdown = dividend.build_dividend_event_authority_candidate_markdown_v1(
        _candidate()
    )

    for section in [
        "## Title",
        "## Purpose",
        "## Source Corporate-Action Plan Approval",
        "## Source Split Candidate Review",
        "## Target Universe",
        "## Dividend Event Authority Candidate Objective",
        "## Per-Ticker Dividend Event Candidate Entries",
        "## Dividend Event Evidence Requirements",
        "## Dividend Policy Reconciliation Requirements",
        "## Future Dividend Provider Request Policy",
        "## Future Dividend Authority Chain",
        "## Future Corporate-Action Readiness Chain",
        "## Future Gates",
        "## Risk Controls",
        "## Dividend Authority Boundary",
        "## Split Boundary",
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
    result = dividend.write_dividend_event_authority_candidate_v1(tmp_path)
    payload = json.loads((tmp_path / result["filename"]).read_text(encoding="utf-8"))

    assert result["filename"] == "dividend_event_authority_candidate_v1.json"
    assert payload["artifact_kind"] == (
        dividend.ARTIFACT_KIND_DIVIDEND_EVENT_AUTHORITY_CANDIDATE
    )
    with pytest.raises(dividend.DividendEventAuthorityCandidateError):
        dividend.write_dividend_event_authority_candidate_v1(tmp_path)


def test_top_level_services_exports_are_available():
    candidate = _candidate()

    assert services.ARTIFACT_KIND_DIVIDEND_EVENT_AUTHORITY_CANDIDATE == (
        dividend.ARTIFACT_KIND_DIVIDEND_EVENT_AUTHORITY_CANDIDATE
    )
    assert services.DIVIDEND_EVENT_AUTHORITY_READY_FOR_OPERATOR_REVIEW == (
        dividend.DIVIDEND_EVENT_AUTHORITY_READY_FOR_OPERATOR_REVIEW
    )
    assert services.dividend_event_authority_candidate_digest_v1(candidate) == (
        candidate["dividend_event_authority_candidate_digest"]
    )
    assert services.per_ticker_dividend_event_candidate_digest_v1(
        candidate["per_ticker_dividend_event_candidate_entries"][0]
    ) == candidate["per_ticker_dividend_event_candidate_entries"][0][
        "per_ticker_dividend_event_candidate_digest"
    ]
    assert services.validate_dividend_event_authority_candidate_v1(candidate)[
        "status"
    ] == "DIVIDEND_EVENT_AUTHORITY_CANDIDATE_VALID"
