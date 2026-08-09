from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest

from marketflow import services
from marketflow.services import live_ticker_validation_candidate_service as candidate


def _candidate() -> dict[str, Any]:
    return candidate.build_live_ticker_validation_candidate_v1()


def _redigest(payload: dict[str, Any]) -> dict[str, Any]:
    payload["validation_checklist"] = candidate._checklist(payload)
    payload["validation_summary"] = candidate._summary(payload["validation_checklist"])
    payload["live_ticker_validation_candidate_digest"] = (
        candidate.live_ticker_validation_candidate_digest_v1(payload)
    )
    return payload


def test_candidate_builds_offline_without_provider_calls(monkeypatch: pytest.MonkeyPatch):
    def fail_if_called(*args, **kwargs):
        raise AssertionError("candidate must not rebuild approval or touch provider paths")

    monkeypatch.setattr(
        candidate.selection_approval,
        "build_ticker_universe_selection_approved_v1",
        fail_if_called,
    )

    built = _candidate()

    assert built["created_offline"] is True
    assert built["provider_requests_made"] is False


def test_artifact_kind_is_live_ticker_validation_candidate():
    assert _candidate()["artifact_kind"] == candidate.ARTIFACT_KIND_LIVE_TICKER_VALIDATION_CANDIDATE


def test_candidate_status_is_ready_for_operator_review():
    assert _candidate()["candidate_status"] == (
        candidate.LIVE_TICKER_VALIDATION_READY_FOR_OPERATOR_REVIEW
    )


def test_ticker_universe_selection_approval_digest_is_bound():
    assert _candidate()["ticker_universe_selection_approval_digest"] == (
        candidate.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST
    )


def test_ticker_universe_candidate_digest_is_bound():
    assert _candidate()["ticker_universe_selection_candidate_digest"] == (
        candidate.EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_DIGEST
    )


def test_ticker_universe_review_digest_is_bound():
    assert _candidate()["ticker_universe_selection_candidate_review_package_digest"] == (
        candidate.EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_REVIEW_PACKAGE_DIGEST
    )


def test_scope_expansion_review_digest_is_bound():
    assert _candidate()["predictive_evidence_scope_expansion_plan_candidate_review_package_digest"] == (
        candidate.EXPECTED_SCOPE_EXPANSION_REVIEW_PACKAGE_DIGEST
    )


def test_approved_ticker_count_is_12():
    assert _candidate()["approved_expanded_ticker_count"] == 12


def test_approved_tickers_match_selection_approval_list():
    assert _candidate()["approved_expanded_ticker_universe"] == (
        candidate.APPROVED_EXPANDED_TICKER_UNIVERSE
    )


def test_validation_target_count_is_12():
    assert _candidate()["validation_target_count"] == 12


def test_validation_targets_are_all_future_validation_only():
    assert {entry["validation_target_status"] for entry in _candidate()["validation_target_entries"]} == {
        candidate.APPROVED_FOR_FUTURE_VALIDATION_ONLY
    }


@pytest.mark.parametrize(
    "field",
    [
        "provider_requests_made",
        "provider_request_authorized",
        "live_provider_transport_enabled",
        "live_ticker_validation_authorized",
        "live_ticker_validation_performed",
        "new_ticker_authority_created",
        "new_ticker_acquisition_authorized",
        "dataset_generation_authorized",
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
        "live_ticker_validation_artifact_created",
        "live_validation_results_created",
        "new_ticker_authority_artifact_created",
        "acquisition_authorization_artifact_created",
        "dataset_generation_authorization_created",
        "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_artifact_created",
        "runtime_migration_approval_artifact_created",
    ],
)
def test_execution_authority_and_follow_on_artifact_flags_remain_false(field: str):
    assert _candidate()[field] is False


def test_validation_target_provider_request_status_is_not_requested():
    assert {entry["provider_request_status"] for entry in _candidate()["validation_target_entries"]} == {
        candidate.NOT_REQUESTED
    }


def test_validation_target_live_validation_status_is_not_performed():
    assert {entry["live_validation_status"] for entry in _candidate()["validation_target_entries"]} == {
        candidate.NOT_PERFORMED
    }


def test_validation_target_listing_security_exchange_and_active_statuses_are_not_verified():
    entries = _candidate()["validation_target_entries"]

    for field in (
        "listing_status",
        "security_type_status",
        "exchange_status",
        "active_status",
        "delisting_status",
        "tradability_status",
        "corporate_action_data_availability_status",
        "historical_aggregate_data_availability_status",
    ):
        assert {entry[field] for entry in entries} == {candidate.NOT_VERIFIED}


def test_validation_target_authority_statuses_are_not_created():
    entries = _candidate()["validation_target_entries"]

    for field in (
        "identity_authority_status",
        "split_event_authority_status",
        "dividend_event_authority_status",
        "acquisition_authority_status",
        "canonical_dataset_authority_status",
        "registry_approval_status",
    ):
        assert {entry[field] for entry in entries} == {candidate.NOT_CREATED}


def test_validation_target_runtime_strategy_paper_and_broker_are_not_authorized():
    entries = _candidate()["validation_target_entries"]

    for field in (
        "research_use_status",
        "runtime_use",
        "strategy_use",
        "paper_trading",
        "broker_execution",
    ):
        assert {entry[field] for entry in entries} == {candidate.NOT_AUTHORIZED}


def test_planned_validation_checks_are_defined():
    checks = _candidate()["planned_validation_checks"]

    assert [item["check_name"] for item in checks] == [
        name for name, _purpose in candidate.PLANNED_VALIDATION_CHECKS
    ]
    assert {item["performed_now"] for item in checks} == {False}
    assert {item["operator_approval_required_before_execution"] for item in checks} == {True}


def test_provider_request_policy_requires_separate_approval():
    policy = _candidate()["provider_request_policy"]

    assert policy["future_provider_request_policy_status"] == (
        candidate.PLANNED_REQUIRES_SEPARATE_APPROVAL
    )
    assert policy["allowed_future_request_type"] == candidate.READ_ONLY_VALIDATION_REQUESTS_ONLY
    assert policy["api_key_handling"] == candidate.DO_NOT_STORE_KEYS_OR_PRINT_KEYS
    assert policy["raw_payload_policy"] == candidate.DO_NOT_COMMIT_RAW_PROVIDER_PAYLOADS
    assert policy["provider_result_authority"] == (
        candidate.VALIDATION_RESULTS_ONLY_NOT_ACQUISITION_AUTHORITY
    )


def test_planned_outputs_are_not_generated_and_research_only():
    outputs = _candidate()["planned_outputs"]

    assert [item["output_id"] for item in outputs] == candidate.PLANNED_OUTPUT_IDS
    assert {item["generation_status"] for item in outputs} == {candidate.PLANNED_NOT_GENERATED}
    assert {item["actionability_label"] for item in outputs} == {
        candidate.RESEARCH_ONLY_NON_ACTIONABLE
    }


def test_future_gates_are_defined():
    built = _candidate()

    assert built["future_gates"] == candidate.FUTURE_GATES
    assert built["future_gate_count"] == len(candidate.FUTURE_GATES)


def test_risk_controls_are_defined():
    built = _candidate()

    assert built["risk_controls"] == candidate.RISK_CONTROLS
    assert built["risk_control_count"] == len(candidate.RISK_CONTROLS)


def test_predictive_usefulness_remains_not_accepted():
    built = _candidate()

    assert built["predictive_usefulness"] == "not accepted"
    assert built["predictive_usefulness_acceptance_ready"] is False
    assert built["predictive_usefulness_acceptance_candidate_created"] is False


def test_profitability_remains_not_accepted():
    built = _candidate()

    assert built["profitability"] == "not accepted"
    assert built["profitability_acceptance_ready"] is False


def test_runtime_and_execution_use_remain_not_authorized():
    built = _candidate()

    assert built["runtime_use"] == candidate.NOT_AUTHORIZED
    assert built["strategy_use"] == candidate.NOT_AUTHORIZED
    assert built["paper_trading"] == candidate.NOT_AUTHORIZED
    assert built["broker_execution"] == candidate.NOT_AUTHORIZED


def test_ready_for_live_ticker_validation_approval_remains_false():
    assert _candidate()["validation_summary"]["ready_for_live_ticker_validation_approval"] is False


def test_checklist_contains_all_required_check_ids():
    assert [item["check_id"] for item in _candidate()["validation_checklist"]] == (
        candidate.REQUIRED_CHECK_IDS
    )


def test_all_checks_pass_for_accepted_candidate():
    assert {item["status"] for item in _candidate()["validation_checklist"]} == {
        candidate.PASS
    }


def test_summary_counts_total_passed_and_failed_correctly():
    summary = _candidate()["validation_summary"]

    assert summary["total_checks"] == len(candidate.REQUIRED_CHECK_IDS)
    assert summary["passed_checks"] == len(candidate.REQUIRED_CHECK_IDS)
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["ready_for_operator_review"] is True


def test_candidate_digest_is_deterministic_and_expected():
    assert _candidate()["live_ticker_validation_candidate_digest"] == (
        "7d4bd0b944cce2fd6be6e242683befba3ea432ddfec079eeac129722942587e7"
    )
    assert _candidate()["live_ticker_validation_candidate_digest"] == _candidate()[
        "live_ticker_validation_candidate_digest"
    ]


def test_validator_accepts_valid_candidate():
    validation = candidate.validate_live_ticker_validation_candidate_v1(_candidate())

    assert validation["status"] == "LIVE_TICKER_VALIDATION_CANDIDATE_VALID"
    assert validation["ready_for_operator_review"] is True
    assert validation["ready_for_live_ticker_validation_approval"] is False


@pytest.mark.parametrize(
    "field",
    [
        "provider_requests_made",
        "provider_request_authorized",
        "live_provider_transport_enabled",
        "live_ticker_validation_authorized",
        "live_ticker_validation_performed",
        "new_ticker_authority_created",
        "new_ticker_acquisition_authorized",
        "dataset_generation_authorized",
        "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed",
        "predictive_experiment_rerun_authorized",
        "predictive_experiment_rerun_performed",
        "walk_forward_rerun_performed",
        "label_regeneration_performed",
        "feature_matrix_regeneration_performed",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
        "runtime_migration_approved",
        "automatic_stitching",
    ],
)
def test_validator_rejects_forbidden_true_flags(field: str):
    payload = deepcopy(_candidate())
    payload[field] = True

    with pytest.raises(candidate.LiveTickerValidationCandidateError):
        candidate.validate_live_ticker_validation_candidate_v1(payload)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("approved_expanded_ticker_count", 11),
        ("validation_target_count", 11),
    ],
)
def test_validator_rejects_wrong_counts(field: str, value: int):
    payload = deepcopy(_candidate())
    payload[field] = value
    _redigest(payload)

    with pytest.raises(candidate.LiveTickerValidationCandidateError):
        candidate.validate_live_ticker_validation_candidate_v1(payload)


def test_validator_rejects_validation_targets_differing_from_approved_universe():
    payload = deepcopy(_candidate())
    payload["validation_target_entries"][0]["ticker"] = "AAPL"
    _redigest(payload)

    with pytest.raises(candidate.LiveTickerValidationCandidateError):
        candidate.validate_live_ticker_validation_candidate_v1(payload)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("provider_request_status", "REQUESTED"),
        ("live_validation_status", "PERFORMED"),
        ("listing_status", "VERIFIED"),
        ("security_type_status", "VERIFIED"),
        ("exchange_status", "VERIFIED"),
        ("active_status", "VERIFIED"),
        ("identity_authority_status", "CREATED"),
        ("acquisition_authority_status", "CREATED"),
        ("runtime_use", "AUTHORIZED"),
        ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
    ],
)
def test_validator_rejects_invalid_validation_target_statuses(field: str, value: str):
    payload = deepcopy(_candidate())
    payload["validation_target_entries"][0][field] = value
    _redigest(payload)

    with pytest.raises(candidate.LiveTickerValidationCandidateError):
        candidate.validate_live_ticker_validation_candidate_v1(payload)


@pytest.mark.parametrize(
    "field",
    [
        "planned_validation_checks",
        "provider_request_policy",
        "future_gates",
        "risk_controls",
    ],
)
def test_validator_rejects_missing_planning_sections(field: str):
    payload = deepcopy(_candidate())
    payload.pop(field)
    _redigest(payload)

    with pytest.raises(candidate.LiveTickerValidationCandidateError):
        candidate.validate_live_ticker_validation_candidate_v1(payload)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("predictive_usefulness", "accepted"),
        ("profitability", "accepted"),
        ("runtime_use", "AUTHORIZED"),
        ("strategy_use", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
    ],
)
def test_validator_rejects_forbidden_authorization_values(field: str, value: str):
    payload = deepcopy(_candidate())
    payload[field] = value

    with pytest.raises(candidate.LiveTickerValidationCandidateError):
        candidate.validate_live_ticker_validation_candidate_v1(payload)


@pytest.mark.parametrize(
    "field",
    [
        "ticker_universe_selection_approval_digest",
        "ticker_universe_selection_candidate_digest",
    ],
)
def test_validator_rejects_missing_source_digests(field: str):
    payload = deepcopy(_candidate())
    payload.pop(field)
    _redigest(payload)

    with pytest.raises(candidate.LiveTickerValidationCandidateError):
        candidate.validate_live_ticker_validation_candidate_v1(payload)


def test_validator_rejects_artifact_kind_mismatch():
    payload = deepcopy(_candidate())
    payload["artifact_kind"] = "WRONG"

    with pytest.raises(candidate.LiveTickerValidationCandidateError):
        candidate.validate_live_ticker_validation_candidate_v1(payload)


def test_validator_rejects_candidate_status_mismatch():
    payload = deepcopy(_candidate())
    payload["candidate_status"] = "LIVE_TICKER_VALIDATION_APPROVED"

    with pytest.raises(candidate.LiveTickerValidationCandidateError):
        candidate.validate_live_ticker_validation_candidate_v1(payload)


def test_markdown_writer_includes_required_sections():
    markdown = candidate.build_live_ticker_validation_candidate_markdown_v1(_candidate())

    for section in [
        "## Title",
        "## Purpose",
        "## Source Ticker Universe Approval",
        "## Validation Target Universe",
        "## Planned Validation Checks",
        "## Provider Request Policy",
        "## Planned Outputs",
        "## Future Gates",
        "## Risk Controls",
        "## Validation Boundary",
        "## Acquisition Boundary",
        "## Predictive/Profitability Boundary",
        "## Runtime Boundary",
        "## Checklist Summary",
        "## Guardrails",
    ]:
        assert section in markdown


def test_writer_rejects_existing_output_file(tmp_path: Path):
    output_path = tmp_path / "live_ticker_validation_candidate_v1.json"
    output_path.write_text("{}", encoding="utf-8")

    with pytest.raises(candidate.LiveTickerValidationCandidateError):
        candidate.write_live_ticker_validation_candidate_v1(tmp_path)


def test_writer_creates_non_overwriting_json_file(tmp_path: Path):
    result = candidate.write_live_ticker_validation_candidate_v1(tmp_path)

    assert result["filename"] == "live_ticker_validation_candidate_v1.json"
    assert Path(result["path"]).exists()
    assert result["payload_byte_size"] > 0


def test_public_exports_are_available():
    assert services.ARTIFACT_KIND_LIVE_TICKER_VALIDATION_CANDIDATE == (
        candidate.ARTIFACT_KIND_LIVE_TICKER_VALIDATION_CANDIDATE
    )
    assert services.LIVE_TICKER_VALIDATION_READY_FOR_OPERATOR_REVIEW == (
        candidate.LIVE_TICKER_VALIDATION_READY_FOR_OPERATOR_REVIEW
    )
    assert services.build_live_ticker_validation_candidate_v1 is (
        candidate.build_live_ticker_validation_candidate_v1
    )
    assert services.validate_live_ticker_validation_candidate_v1 is (
        candidate.validate_live_ticker_validation_candidate_v1
    )
    assert services.write_live_ticker_validation_candidate_v1 is (
        candidate.write_live_ticker_validation_candidate_v1
    )
