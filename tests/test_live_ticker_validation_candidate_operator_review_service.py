from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest

from marketflow import services
from marketflow.services import live_ticker_validation_candidate_operator_review_service as review
from marketflow.services import live_ticker_validation_candidate_service as candidate


EXPECTED_REVIEW_PACKAGE_DIGEST = (
    "c38b723df9a66e94ff82696cf8c88aa5008e915e7fc42b2a8a760ea61623b3fc"
)


def _package() -> dict[str, Any]:
    return review.build_live_ticker_validation_candidate_review_package_v1()


def _redigest(payload: dict[str, Any]) -> dict[str, Any]:
    payload["review_checklist"] = review._checklist(payload)
    payload["review_summary"] = review._summary(payload["review_checklist"])
    payload["live_ticker_validation_candidate_review_package_digest"] = (
        review.live_ticker_validation_candidate_review_package_digest_v1(payload)
    )
    return payload


def test_review_package_builds_offline_without_rebuilding_candidate_or_provider_paths(
    monkeypatch: pytest.MonkeyPatch,
):
    def fail_if_called(*args, **kwargs):
        raise AssertionError("review package must bind recorded candidate evidence")

    monkeypatch.setattr(candidate, "build_live_ticker_validation_candidate_v1", fail_if_called)
    monkeypatch.setattr(
        candidate.selection_approval,
        "build_ticker_universe_selection_approved_v1",
        fail_if_called,
    )

    built = _package()

    assert built["created_offline"] is True
    assert built["provider_requests_made_in_review"] is False
    assert built["live_ticker_validation_candidate_binding_mode"] == (
        review.LIVE_TICKER_VALIDATION_CANDIDATE_STATUS_BINDING
    )


def test_review_package_accepts_valid_candidate_object_binding():
    built_candidate = candidate.build_live_ticker_validation_candidate_v1()

    built = review.build_live_ticker_validation_candidate_review_package_v1(built_candidate)

    assert built["live_ticker_validation_candidate_binding_mode"] == (
        review.LIVE_TICKER_VALIDATION_CANDIDATE_OBJECT_BINDING
    )
    assert built["reviewed_live_ticker_validation_candidate_digest"] == (
        review.EXPECTED_LIVE_TICKER_VALIDATION_CANDIDATE_DIGEST
    )


def test_artifact_kind_and_status_are_review_package_ready():
    built = _package()

    assert built["artifact_kind"] == (
        review.ARTIFACT_KIND_LIVE_TICKER_VALIDATION_CANDIDATE_REVIEW_PACKAGE
    )
    assert built["review_status"] == (
        review.LIVE_TICKER_VALIDATION_CANDIDATE_REVIEW_PACKAGE_READY
    )
    assert built["schema_version"] == (
        review.SCHEMA_VERSION_LIVE_TICKER_VALIDATION_CANDIDATE_REVIEW_V1
    )


def test_operator_decision_is_required_and_not_recorded():
    built = _package()

    assert built["operator_decision_required"] is True
    assert built["operator_decision"] is None
    assert built["review_summary"]["ready_for_operator_assessment"] is True
    assert built["review_summary"]["ready_for_live_ticker_validation_approval"] is False


def test_reviewed_candidate_evidence_is_bound_exactly():
    built = _package()

    assert built["reviewed_live_ticker_validation_candidate_kind"] == (
        candidate.ARTIFACT_KIND_LIVE_TICKER_VALIDATION_CANDIDATE
    )
    assert built["reviewed_live_ticker_validation_candidate_status"] == (
        candidate.LIVE_TICKER_VALIDATION_READY_FOR_OPERATOR_REVIEW
    )
    assert built["reviewed_live_ticker_validation_candidate_digest"] == (
        review.EXPECTED_LIVE_TICKER_VALIDATION_CANDIDATE_DIGEST
    )
    assert built["reviewed_live_ticker_validation_candidate_checklist_total"] == 64
    assert built["reviewed_live_ticker_validation_candidate_checklist_passed"] == 64
    assert built["reviewed_live_ticker_validation_candidate_checklist_failed"] == 0
    assert built["reviewed_live_ticker_validation_candidate_blocker_count"] == 0


def test_source_evidence_digests_are_bound():
    built = _package()

    assert built["ticker_universe_selection_approval_digest"] == (
        review.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST
    )
    assert built["ticker_universe_selection_candidate_digest"] == (
        review.EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_DIGEST
    )
    assert built["ticker_universe_selection_candidate_review_package_digest"] == (
        review.EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_REVIEW_PACKAGE_DIGEST
    )
    assert built["predictive_evidence_scope_expansion_plan_candidate_review_package_digest"] == (
        review.EXPECTED_SCOPE_EXPANSION_REVIEW_PACKAGE_DIGEST
    )
    assert built["predictive_evidence_scope_expansion_plan_candidate_digest"] == (
        review.EXPECTED_SCOPE_EXPANSION_CANDIDATE_DIGEST
    )
    assert built["additional_predictive_evidence_plan_candidate_review_package_digest"] == (
        review.EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_REVIEW_PACKAGE_DIGEST
    )
    assert built["additional_predictive_evidence_plan_candidate_digest"] == (
        review.EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE_DIGEST
    )
    assert built[
        "predictive_usefulness_acceptance_readiness_candidate_review_package_digest"
    ] == review.EXPECTED_ACCEPTANCE_READINESS_REVIEW_PACKAGE_DIGEST
    assert built["predictive_usefulness_acceptance_readiness_candidate_digest"] == (
        review.EXPECTED_ACCEPTANCE_READINESS_CANDIDATE_DIGEST
    )


def test_validation_target_universe_is_approved_for_future_validation_only():
    built = _package()
    entries = built["validation_target_entries"]

    assert built["approved_expanded_ticker_universe"] == review.APPROVED_EXPANDED_TICKER_UNIVERSE
    assert built["approved_expanded_ticker_count"] == 12
    assert built["validation_target_count"] == 12
    assert [entry["ticker"] for entry in entries] == [
        "MSFT",
        "NVDA",
        "AMZN",
        "GOOGL",
        "META",
        "TSLA",
        "JPM",
        "XOM",
        "JNJ",
        "WMT",
        "CAT",
        "LMT",
    ]
    assert {entry["validation_target_status"] for entry in entries} == {
        review.APPROVED_FOR_FUTURE_VALIDATION_ONLY
    }


def test_validation_target_statuses_are_all_not_requested_or_not_verified():
    entries = _package()["validation_target_entries"]

    for field, expected in {
        "provider_request_status": review.NOT_REQUESTED,
        "live_validation_status": review.NOT_PERFORMED,
        "listing_status": review.NOT_VERIFIED,
        "security_type_status": review.NOT_VERIFIED,
        "exchange_status": review.NOT_VERIFIED,
        "active_status": review.NOT_VERIFIED,
        "delisting_status": review.NOT_VERIFIED,
        "tradability_status": review.NOT_VERIFIED,
        "corporate_action_data_availability_status": review.NOT_VERIFIED,
        "historical_aggregate_data_availability_status": review.NOT_VERIFIED,
    }.items():
        assert {entry[field] for entry in entries} == {expected}


def test_validation_target_authority_and_runtime_statuses_remain_closed():
    entries = _package()["validation_target_entries"]

    for field in (
        "identity_authority_status",
        "split_event_authority_status",
        "dividend_event_authority_status",
        "acquisition_authority_status",
        "canonical_dataset_authority_status",
        "registry_approval_status",
    ):
        assert {entry[field] for entry in entries} == {review.NOT_CREATED}
    for field in (
        "research_use_status",
        "runtime_use",
        "strategy_use",
        "paper_trading",
        "broker_execution",
    ):
        assert {entry[field] for entry in entries} == {review.NOT_AUTHORIZED}


def test_planned_validation_checks_policy_outputs_gates_and_risks_are_bound():
    built = _package()
    policy = built["provider_request_policy"]

    assert built["planned_validation_check_count"] == 11
    assert [item["check_name"] for item in built["planned_validation_checks"]] == [
        name for name, _purpose in review.PLANNED_VALIDATION_CHECKS
    ]
    assert {item["performed_now"] for item in built["planned_validation_checks"]} == {False}
    assert policy["future_provider_request_policy_status"] == (
        review.PLANNED_REQUIRES_SEPARATE_APPROVAL
    )
    assert policy["allowed_future_request_type"] == review.READ_ONLY_VALIDATION_REQUESTS_ONLY
    assert policy["api_key_handling"] == review.DO_NOT_STORE_KEYS_OR_PRINT_KEYS
    assert policy["raw_payload_policy"] == review.DO_NOT_COMMIT_RAW_PROVIDER_PAYLOADS
    assert policy["sanitized_status_doc_required"] is True
    assert policy["rate_limit_policy"] == review.RESPECT_PROVIDER_LIMITS_AND_FAIL_CLOSED
    assert policy["provider_result_authority"] == (
        review.VALIDATION_RESULTS_ONLY_NOT_ACQUISITION_AUTHORITY
    )
    assert built["planned_output_count"] == 6
    assert {item["generation_status"] for item in built["planned_outputs"]} == {
        review.PLANNED_NOT_GENERATED
    }
    assert {item["actionability_label"] for item in built["planned_outputs"]} == {
        review.RESEARCH_ONLY_NON_ACTIONABLE
    }
    assert built["future_gate_count"] == 10
    assert built["risk_control_count"] == 14


@pytest.mark.parametrize(
    "field",
    [
        "provider_requests_made_in_review",
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
        "ready_for_live_ticker_validation_approval",
        "live_ticker_validation_approval_artifact_created",
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
    assert _package()[field] is False


def test_predictive_profitability_and_runtime_use_remain_not_accepted_or_authorized():
    built = _package()

    assert built["predictive_usefulness"] == "not accepted"
    assert built["profitability"] == "not accepted"
    assert built["runtime_use"] == review.NOT_AUTHORIZED
    assert built["strategy_use"] == review.NOT_AUTHORIZED
    assert built["paper_trading"] == review.NOT_AUTHORIZED
    assert built["broker_execution"] == review.NOT_AUTHORIZED


def test_checklist_contains_all_required_check_ids_and_passes():
    checklist = _package()["review_checklist"]

    assert [item["check_id"] for item in checklist] == review.REQUIRED_CHECK_IDS
    assert {item["status"] for item in checklist} == {review.PASS}
    assert len(checklist) == 71


def test_review_summary_counts_total_passed_failed_and_blockers():
    summary = _package()["review_summary"]

    assert summary["total_checks"] == len(review.REQUIRED_CHECK_IDS)
    assert summary["passed_checks"] == len(review.REQUIRED_CHECK_IDS)
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["ready_for_operator_assessment"] is True
    assert summary["ready_for_live_ticker_validation_approval"] is False


def test_review_package_digest_is_deterministic_and_expected():
    assert _package()["live_ticker_validation_candidate_review_package_digest"] == (
        EXPECTED_REVIEW_PACKAGE_DIGEST
    )
    assert _package()["live_ticker_validation_candidate_review_package_digest"] == _package()[
        "live_ticker_validation_candidate_review_package_digest"
    ]


def test_validator_accepts_valid_review_package():
    validation = review.validate_live_ticker_validation_candidate_review_package_v1(_package())

    assert validation["status"] == "LIVE_TICKER_VALIDATION_CANDIDATE_REVIEW_PACKAGE_VALID"
    assert validation["ready_for_operator_assessment"] is True
    assert validation["ready_for_live_ticker_validation_approval"] is False


@pytest.mark.parametrize(
    "field",
    [
        "provider_requests_made_in_review",
        "provider_request_authorized",
        "live_provider_transport_enabled",
        "live_ticker_validation_authorized",
        "live_ticker_validation_performed",
        "ready_for_live_ticker_validation_approval",
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
        "live_ticker_validation_approval_artifact_created",
        "live_ticker_validation_artifact_created",
        "live_validation_results_created",
    ],
)
def test_validator_rejects_forbidden_true_flags(field: str):
    payload = deepcopy(_package())
    payload[field] = True

    with pytest.raises(review.LiveTickerValidationCandidateReviewPackageError):
        review.validate_live_ticker_validation_candidate_review_package_v1(payload)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("approved_expanded_ticker_count", 11),
        ("validation_target_count", 11),
        ("planned_validation_check_count", 10),
        ("planned_output_count", 5),
        ("future_gate_count", 9),
        ("risk_control_count", 13),
    ],
)
def test_validator_rejects_wrong_counts(field: str, value: int):
    payload = deepcopy(_package())
    payload[field] = value
    _redigest(payload)

    with pytest.raises(review.LiveTickerValidationCandidateReviewPackageError):
        review.validate_live_ticker_validation_candidate_review_package_v1(payload)


def test_validator_rejects_validation_targets_differing_from_approved_universe():
    payload = deepcopy(_package())
    payload["validation_target_entries"][0]["ticker"] = "AAPL"
    _redigest(payload)

    with pytest.raises(review.LiveTickerValidationCandidateReviewPackageError):
        review.validate_live_ticker_validation_candidate_review_package_v1(payload)


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
    payload = deepcopy(_package())
    payload["validation_target_entries"][0][field] = value
    _redigest(payload)

    with pytest.raises(review.LiveTickerValidationCandidateReviewPackageError):
        review.validate_live_ticker_validation_candidate_review_package_v1(payload)


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
    payload = deepcopy(_package())
    payload.pop(field)
    _redigest(payload)

    with pytest.raises(review.LiveTickerValidationCandidateReviewPackageError):
        review.validate_live_ticker_validation_candidate_review_package_v1(payload)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("predictive_usefulness", "accepted"),
        ("profitability", "accepted"),
        ("runtime_use", "AUTHORIZED"),
        ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
    ],
)
def test_validator_rejects_forbidden_authorization_values(field: str, value: str):
    payload = deepcopy(_package())
    payload[field] = value

    with pytest.raises(review.LiveTickerValidationCandidateReviewPackageError):
        review.validate_live_ticker_validation_candidate_review_package_v1(payload)


@pytest.mark.parametrize(
    "field",
    [
        "reviewed_live_ticker_validation_candidate_digest",
        "ticker_universe_selection_approval_digest",
        "ticker_universe_selection_candidate_digest",
    ],
)
def test_validator_rejects_missing_source_or_candidate_digests(field: str):
    payload = deepcopy(_package())
    payload.pop(field)
    _redigest(payload)

    with pytest.raises(review.LiveTickerValidationCandidateReviewPackageError):
        review.validate_live_ticker_validation_candidate_review_package_v1(payload)


def test_validator_rejects_artifact_kind_mismatch():
    payload = deepcopy(_package())
    payload["artifact_kind"] = "WRONG"

    with pytest.raises(review.LiveTickerValidationCandidateReviewPackageError):
        review.validate_live_ticker_validation_candidate_review_package_v1(payload)


def test_validator_rejects_review_status_mismatch():
    payload = deepcopy(_package())
    payload["review_status"] = "LIVE_TICKER_VALIDATION_APPROVED"

    with pytest.raises(review.LiveTickerValidationCandidateReviewPackageError):
        review.validate_live_ticker_validation_candidate_review_package_v1(payload)


def test_markdown_writer_includes_required_sections():
    markdown = review.build_live_ticker_validation_candidate_review_markdown_v1(_package())

    for section in [
        "## Title",
        "## Purpose",
        "## Review Package",
        "## Reviewed Candidate Evidence",
        "## Source Evidence",
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
    output_path = tmp_path / "live_ticker_validation_candidate_review_package_v1.json"
    output_path.write_text("{}", encoding="utf-8")

    with pytest.raises(review.LiveTickerValidationCandidateReviewPackageError):
        review.write_live_ticker_validation_candidate_review_package_v1(tmp_path)


def test_writer_creates_non_overwriting_json_file(tmp_path: Path):
    result = review.write_live_ticker_validation_candidate_review_package_v1(tmp_path)

    assert result["filename"] == "live_ticker_validation_candidate_review_package_v1.json"
    assert Path(result["path"]).exists()
    assert result["payload_byte_size"] > 0
    assert result["provider_requests_made_in_review"] is False


def test_public_exports_are_available():
    assert services.ARTIFACT_KIND_LIVE_TICKER_VALIDATION_CANDIDATE_REVIEW_PACKAGE == (
        review.ARTIFACT_KIND_LIVE_TICKER_VALIDATION_CANDIDATE_REVIEW_PACKAGE
    )
    assert services.LIVE_TICKER_VALIDATION_CANDIDATE_REVIEW_PACKAGE_READY == (
        review.LIVE_TICKER_VALIDATION_CANDIDATE_REVIEW_PACKAGE_READY
    )
    assert services.build_live_ticker_validation_candidate_review_package_v1 is (
        review.build_live_ticker_validation_candidate_review_package_v1
    )
    assert services.validate_live_ticker_validation_candidate_review_package_v1 is (
        review.validate_live_ticker_validation_candidate_review_package_v1
    )
    assert services.write_live_ticker_validation_candidate_review_package_v1 is (
        review.write_live_ticker_validation_candidate_review_package_v1
    )
