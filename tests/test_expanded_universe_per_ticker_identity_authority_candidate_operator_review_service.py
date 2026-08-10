from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from marketflow.historical_data.artifacts import canonical_json_bytes, sha256_bytes
from marketflow.services import (
    expanded_universe_per_ticker_identity_authority_candidate_operator_review_service as review,
)


def _write_json(path: Path, payload: dict[str, Any]) -> str:
    data = canonical_json_bytes(payload)
    path.write_bytes(data)
    return sha256_bytes(data)


def _fixture_output_root(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> Path:
    root = tmp_path / "source_outputs"
    root.mkdir(exist_ok=True)
    tickers = review.VALIDATION_TARGET_UNIVERSE
    results = [
        {
            "ticker": ticker,
            "live_validation_status": review.candidate_service.plan_review.plan.VALIDATED_READ_ONLY,
            "active_status": review.candidate_service.plan_review.plan.VALIDATED_READ_ONLY,
            "provider_endpoint": f"/v3/reference/tickers/{ticker}",
            "provider_response_digest": f"{ticker.lower()}-provider-digest",
            "sanitized_validation_digest": f"{ticker.lower()}-sanitized-digest",
        }
        for ticker in tickers
    ]
    receipts = [
        {
            "ticker": ticker,
            "provider_name": "Massive.com",
            "provider_response_digest": f"{ticker.lower()}-provider-digest",
            "raw_payload_committed": False,
            "raw_response_stored": False,
            "api_key_stored_or_printed": False,
        }
        for ticker in tickers
    ]
    payloads = {
        "live_ticker_validation_run_manifest.json": {
            "validation_target_universe": tickers,
            "selected_endpoint": "/v3/reference/tickers/{ticker}",
        },
        "ticker_validation_results.json": {"results": results},
        "provider_request_receipts_sanitized.json": {
            "provider_request_receipts": receipts
        },
        "validation_summary.json": {
            "validation_target_count": 12,
            "validated_read_only_count": 12,
        },
        "validation_failure_reason_inventory.json": {"failure_count": 0},
        "operator_review_summary.json": {"operator_review_status": "READY"},
    }
    digests = {
        name: _write_json(root / name, payload)
        for name, payload in payloads.items()
    }
    monkeypatch.setattr(review.candidate_service, "EXPECTED_SOURCE_OUTPUT_DIGESTS", digests)
    return root


def _candidate(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    return review.candidate_service.build_expanded_universe_per_ticker_identity_authority_candidate_v1(
        output_root=_fixture_output_root(tmp_path, monkeypatch)
    )


def _package(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    return review.build_expanded_universe_per_ticker_identity_authority_candidate_review_package_v1(
        candidate=_candidate(tmp_path, monkeypatch)
    )


def _mutated_package(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    field: str,
    value: Any,
) -> dict[str, Any]:
    package = _package(tmp_path, monkeypatch)
    package[field] = value
    return package


def test_review_package_builds_offline_without_provider_calls(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    def fail_provider_call(*_args, **_kwargs):  # pragma: no cover
        raise AssertionError("provider path must not be called")

    monkeypatch.setattr(
        review.candidate_service.plan_review.plan.results_review.provider,
        "fetch_massive_ticker_details_v1",
        fail_provider_call,
    )

    package = _package(tmp_path, monkeypatch)

    assert package["created_offline"] is True
    assert package["provider_requests_made_in_review"] is False
    assert package["live_validation_rerun_performed"] is False
    assert package["live_provider_transport_enabled_in_review"] is False
    assert package["source_output_file_reinspection_performed"] is False


def test_artifact_kind_status_schema_and_binding_mode_are_exact(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    package = _package(tmp_path, monkeypatch)

    assert package["artifact_kind"] == (
        review.ARTIFACT_KIND_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_CANDIDATE_REVIEW_PACKAGE
    )
    assert package["review_status"] == (
        review.EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_READY
    )
    assert package["schema_version"] == (
        review.SCHEMA_VERSION_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_CANDIDATE_REVIEW_V1
    )
    assert package["identity_authority_candidate_binding_mode"] == (
        review.EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_CANDIDATE_OBJECT_BINDING
    )


def test_status_bound_review_package_binds_recorded_candidate_digest(
    monkeypatch: pytest.MonkeyPatch,
):
    def fail_provider_call(*_args, **_kwargs):  # pragma: no cover
        raise AssertionError("provider path must not be called")

    monkeypatch.setattr(
        review.candidate_service.plan_review.plan.results_review.provider,
        "fetch_massive_ticker_details_v1",
        fail_provider_call,
    )

    package = review.build_expanded_universe_per_ticker_identity_authority_candidate_review_package_v1()

    assert package["identity_authority_candidate_binding_mode"] == (
        review.EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_CANDIDATE_STATUS_BINDING
    )
    assert package["reviewed_identity_authority_candidate_digest"] == (
        review.EXPECTED_IDENTITY_AUTHORITY_CANDIDATE_DIGEST
    )
    assert package["identity_authority_candidate_digest"] == (
        review.EXPECTED_IDENTITY_AUTHORITY_CANDIDATE_DIGEST
    )


def test_reviewed_candidate_evidence_is_bound(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    package = _package(tmp_path, monkeypatch)

    assert package["reviewed_identity_authority_candidate_kind"] == (
        review.candidate_service.ARTIFACT_KIND_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_CANDIDATE
    )
    assert package["reviewed_identity_authority_candidate_status"] == (
        review.candidate_service.EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_READY_FOR_OPERATOR_REVIEW
    )
    assert package["reviewed_identity_authority_candidate_digest"] == (
        package["identity_authority_candidate_digest"]
    )
    assert len(package["reviewed_identity_authority_candidate_digest"]) == 64
    assert package["reviewed_identity_authority_candidate_checklist_total"] == 75
    assert package["reviewed_identity_authority_candidate_checklist_passed"] == 75
    assert package["reviewed_identity_authority_candidate_checklist_failed"] == 0
    assert package["reviewed_identity_authority_candidate_blocker_count"] == 0


def test_source_evidence_digest_chain_is_bound(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    package = _package(tmp_path, monkeypatch)

    assert package["identity_authority_candidate_digest"] == (
        package["reviewed_identity_authority_candidate_digest"]
    )
    assert len(package["identity_authority_candidate_digest"]) == 64
    assert package["identity_authority_plan_candidate_review_package_digest"] == (
        review.candidate_service.EXPECTED_IDENTITY_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST
    )
    assert package["identity_authority_plan_candidate_digest"] == (
        review.candidate_service.EXPECTED_IDENTITY_AUTHORITY_PLAN_CANDIDATE_DIGEST
    )
    assert package["live_ticker_validation_results_review_package_digest"] == (
        review.candidate_service.plan_review.plan.EXPECTED_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_DIGEST
    )
    assert package["live_ticker_validation_execution_digest"] == (
        review.candidate_service.plan_review.plan.EXPECTED_LIVE_TICKER_VALIDATION_EXECUTION_DIGEST
    )
    assert package["live_ticker_validation_approval_digest"] == (
        review.candidate_service.plan_review.plan.EXPECTED_LIVE_TICKER_VALIDATION_APPROVAL_DIGEST
    )
    assert package["ticker_universe_selection_approval_digest"] == (
        review.candidate_service.plan_review.plan.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST
    )


def test_target_universe_and_validation_summary_are_preserved(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    package = _package(tmp_path, monkeypatch)

    assert package["target_universe_count"] == 12
    assert package["target_universe"] == review.VALIDATION_TARGET_UNIVERSE
    assert package["validated_universe"] == review.VALIDATION_TARGET_UNIVERSE
    assert package["all_targets_validated_read_only"] is True
    assert package["validated_read_only_count"] == 12
    assert package["provider_request_count"] == 12
    assert package["successful_provider_response_count"] == 12
    assert package["failed_provider_response_count"] == 0


def test_review_scope_and_per_ticker_entries_are_review_only(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    package = _package(tmp_path, monkeypatch)

    assert package["identity_authority_candidate_review_scope"] == review.REVIEW_ONLY_NOT_FREEZE
    assert len(package["per_ticker_identity_candidate_entries"]) == 12
    assert len(package["per_ticker_identity_review_entries"]) == 12
    for entry in package["per_ticker_identity_review_entries"]:
        assert entry["identity_candidate_status"] == (
            review.candidate_service.IDENTITY_CANDIDATE_READY_FOR_OPERATOR_REVIEW
        )
        assert entry["identity_review_status"] == review.REVIEW_PACKAGE_CREATED
        assert entry["identity_authority_scope"] == review.CANDIDATE_REVIEW_ONLY_NOT_FROZEN
        assert entry["identity_authority_created"] is False
        assert entry["identity_freeze_status"] == (
            review.candidate_service.plan_review.plan.NOT_FROZEN
        )
        assert entry["per_ticker_identity_review_status"] == (
            review.READY_FOR_OPERATOR_ASSESSMENT
        )


def test_identity_fields_are_reviewed_with_value_status_structure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    package = _package(tmp_path, monkeypatch)

    assert package["identity_fields_to_bind"] == review.IDENTITY_FIELDS_TO_BIND
    for entry in package["per_ticker_identity_review_entries"]:
        assert set(entry["identity_fields"]) == set(review.IDENTITY_FIELDS_TO_BIND)
        for field in entry["identity_fields"].values():
            assert set(field) == {"value", "status"}
            assert field["status"] in {
                review.candidate_service.AVAILABLE_FROM_SOURCE,
                review.candidate_service.UNAVAILABLE_IN_SOURCE,
            }


def test_unavailable_fields_are_marked_unavailable_and_not_fabricated(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    package = _package(tmp_path, monkeypatch)
    unavailable_count = 0

    for entry in package["per_ticker_identity_review_entries"]:
        for field in entry["identity_fields"].values():
            if field["status"] == review.candidate_service.UNAVAILABLE_IN_SOURCE:
                unavailable_count += 1
                assert field["value"] is None

    assert unavailable_count > 0


def test_provider_response_and_sanitized_validation_digests_are_bound_or_unavailable(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    package = _package(tmp_path, monkeypatch)

    for entry in package["per_ticker_identity_review_entries"]:
        provider_digest = entry["identity_fields"]["provider_response_digest"]
        sanitized_digest = entry["identity_fields"]["sanitized_validation_digest"]
        assert provider_digest["status"] == review.candidate_service.AVAILABLE_FROM_SOURCE
        assert provider_digest["value"]
        assert sanitized_digest["status"] == review.candidate_service.AVAILABLE_FROM_SOURCE
        assert sanitized_digest["value"]


def test_per_ticker_candidate_and_review_digests_are_present_and_deterministic(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    first = _package(tmp_path, monkeypatch)
    second = review.build_expanded_universe_per_ticker_identity_authority_candidate_review_package_v1(
        candidate=_candidate(tmp_path, monkeypatch)
    )

    assert [
        entry["per_ticker_identity_review_digest"]
        for entry in first["per_ticker_identity_review_entries"]
    ] == [
        entry["per_ticker_identity_review_digest"]
        for entry in second["per_ticker_identity_review_entries"]
    ]
    for entry in first["per_ticker_identity_review_entries"]:
        assert entry["per_ticker_identity_candidate_digest"]
        assert entry["per_ticker_identity_review_digest"] == (
            review.per_ticker_identity_review_digest_v1(entry)
        )


def test_field_classification_limitations_future_chain_gates_and_risk_controls_are_defined(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    package = _package(tmp_path, monkeypatch)

    assert package["identity_field_groups"] == review.IDENTITY_FIELD_GROUPS
    assert package["identity_evidence_limitations"] == review.IDENTITY_EVIDENCE_LIMITATIONS
    assert package["future_identity_authority_chain"] == (
        review._future_identity_authority_chain()
    )
    assert package["future_gates"] == review.FUTURE_GATES
    assert package["risk_controls"] == review.RISK_CONTROLS


@pytest.mark.parametrize(
    "field",
    [
        "provider_requests_made_in_review",
        "live_validation_rerun_performed",
        "live_provider_transport_enabled_in_review",
        "source_output_file_reinspection_performed",
        "per_ticker_identity_authority_frozen",
        "identity_authority_created",
        "new_ticker_authority_created",
        "new_ticker_acquisition_authorized",
        "dataset_generation_authorized",
        "corporate_action_authority_created",
        "split_event_authority_created",
        "dividend_event_authority_created",
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
def test_closed_boolean_boundaries_remain_false(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    field: str,
):
    assert _package(tmp_path, monkeypatch)[field] is False


def test_review_created_is_the_only_new_authority_chain_flag(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    package = _package(tmp_path, monkeypatch)

    assert package["per_ticker_identity_authority_candidate_created"] is True
    assert package["per_ticker_identity_authority_review_created"] is True
    assert package["per_ticker_identity_authority_frozen"] is False
    assert package["identity_authority_created"] is False


def test_predictive_profitability_and_runtime_authorizations_remain_closed(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    package = _package(tmp_path, monkeypatch)

    assert package["predictive_usefulness"] == (
        review.acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED
    )
    assert package["profitability"] == review.acquisition.PROFITABILITY_NOT_ACCEPTED
    assert package["runtime_use"] == review.candidate_service.plan_review.plan.NOT_AUTHORIZED
    assert package["strategy_use"] == review.candidate_service.plan_review.plan.NOT_AUTHORIZED
    assert package["paper_trading"] == review.candidate_service.plan_review.plan.NOT_AUTHORIZED
    assert package["broker_execution"] == review.candidate_service.plan_review.plan.NOT_AUTHORIZED
    assert package["review_summary"]["ready_for_identity_freeze"] is False


def test_checklist_contains_all_required_check_ids_and_all_pass(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    package = _package(tmp_path, monkeypatch)

    assert [item["check_id"] for item in package["review_checklist"]] == (
        review.REQUIRED_CHECK_IDS
    )
    assert {item["status"] for item in package["review_checklist"]} == {review.PASS}


def test_summary_counts_total_passed_failed_and_blockers_correctly(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    package = _package(tmp_path, monkeypatch)
    summary = package["review_summary"]

    assert summary["total_checks"] == len(review.REQUIRED_CHECK_IDS)
    assert summary["passed_checks"] == len(review.REQUIRED_CHECK_IDS)
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["ready_for_operator_assessment"] is True
    assert summary["ready_for_identity_freeze"] is False
    assert summary["identity_authority_created"] is False
    assert summary["identity_authority_frozen"] is False
    assert summary["corporate_action_authority_authorized"] is False
    assert summary["acquisition_authorized"] is False
    assert summary["dataset_generation_authorized"] is False
    assert summary["additional_predictive_evidence_execution_authorized"] is False
    assert summary["predictive_usefulness_accepted"] is False
    assert summary["profitability_accepted"] is False
    assert summary["runtime_migration_authorized"] is False
    assert summary["software_runtime_activation_authorized"] is False


def test_review_package_digest_is_deterministic(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    first = _package(tmp_path, monkeypatch)
    second = review.build_expanded_universe_per_ticker_identity_authority_candidate_review_package_v1(
        candidate=_candidate(tmp_path, monkeypatch)
    )

    assert first[
        "expanded_universe_per_ticker_identity_authority_candidate_review_package_digest"
    ] == second[
        "expanded_universe_per_ticker_identity_authority_candidate_review_package_digest"
    ]
    assert first[
        "expanded_universe_per_ticker_identity_authority_candidate_review_package_digest"
    ] == review.expanded_universe_per_ticker_identity_authority_candidate_review_package_digest_v1(
        first
    )


def test_validator_accepts_valid_review_package(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    validation = review.validate_expanded_universe_per_ticker_identity_authority_candidate_review_package_v1(
        _package(tmp_path, monkeypatch)
    )

    assert validation["status"] == (
        "EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_VALID"
    )
    assert validation["ready_for_operator_assessment"] is True
    assert validation["ready_for_identity_freeze"] is False


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("artifact_kind", "EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_FROZEN", "artifact_kind"),
        ("review_status", "FROZEN", "review_status"),
        ("reviewed_identity_authority_candidate_digest", "0" * 64, "candidate_digest"),
        ("reviewed_identity_authority_candidate_status", "FROZEN", "candidate_status"),
        ("provider_requests_made_in_review", True, "provider_requests_made_in_review"),
        ("live_validation_rerun_performed", True, "live_validation_rerun_performed"),
        ("live_provider_transport_enabled_in_review", True, "live_provider_transport_enabled_in_review"),
        ("target_universe_count", 11, "target_universe_count"),
        ("identity_authority_created", True, "identity_authority_created"),
        ("per_ticker_identity_authority_frozen", True, "per_ticker_identity_authority_frozen"),
        ("new_ticker_authority_created", True, "new_ticker_authority_created"),
        ("new_ticker_acquisition_authorized", True, "new_ticker_acquisition_authorized"),
        ("dataset_generation_authorized", True, "dataset_generation_authorized"),
        ("corporate_action_authority_created", True, "corporate_action_authority_created"),
        ("split_event_authority_created", True, "split_event_authority_created"),
        ("dividend_event_authority_created", True, "dividend_event_authority_created"),
        ("acquisition_generation_authorized", True, "acquisition_generation_authorized"),
        ("canonical_dataset_authorized", True, "canonical_dataset_authorized"),
        ("registry_approval_created", True, "registry_approval_created"),
        ("additional_predictive_evidence_execution_authorized", True, "additional_predictive_evidence_execution_authorized"),
        ("predictive_usefulness", "accepted", "predictive_usefulness"),
        ("profitability", "accepted", "profitability"),
        ("runtime_migration_approved", True, "runtime_migration_approved"),
        ("runtime_use", "AUTHORIZED", "runtime_use"),
        ("strategy_use", "AUTHORIZED", "strategy_use"),
        ("broker_execution", "AUTHORIZED", "broker_execution"),
    ],
)
def test_validator_rejects_invalid_top_level_mutations(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    field: str,
    value: Any,
    match: str,
):
    package = _mutated_package(tmp_path, monkeypatch, field, value)

    with pytest.raises(
        review.ExpandedUniversePerTickerIdentityAuthorityCandidateReviewPackageError,
        match=match,
    ):
        review.validate_expanded_universe_per_ticker_identity_authority_candidate_review_package_v1(
            package
        )


def test_validator_rejects_target_universe_mismatch(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    package = _package(tmp_path, monkeypatch)
    package["target_universe"] = package["target_universe"][:-1]

    with pytest.raises(
        review.ExpandedUniversePerTickerIdentityAuthorityCandidateReviewPackageError,
        match="target_universe|target universe",
    ):
        review.validate_expanded_universe_per_ticker_identity_authority_candidate_review_package_v1(
            package
        )


def test_validator_rejects_non_validated_read_only_target(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    package = _package(tmp_path, monkeypatch)
    package["per_ticker_identity_review_entries"][0]["identity_candidate_status"] = "FAILED"

    with pytest.raises(
        review.ExpandedUniversePerTickerIdentityAuthorityCandidateReviewPackageError,
        match="identity_candidate_status",
    ):
        review.validate_expanded_universe_per_ticker_identity_authority_candidate_review_package_v1(
            package
        )


def test_validator_rejects_per_ticker_candidate_count_not_12(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    package = _package(tmp_path, monkeypatch)
    package["per_ticker_identity_candidate_entries"] = (
        package["per_ticker_identity_candidate_entries"][:-1]
    )

    with pytest.raises(
        review.ExpandedUniversePerTickerIdentityAuthorityCandidateReviewPackageError,
        match="per_ticker_identity_candidate_entries",
    ):
        review.validate_expanded_universe_per_ticker_identity_authority_candidate_review_package_v1(
            package
        )


def test_validator_rejects_per_ticker_review_count_not_12(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    package = _package(tmp_path, monkeypatch)
    package["per_ticker_identity_review_entries"] = (
        package["per_ticker_identity_review_entries"][:-1]
    )

    with pytest.raises(
        review.ExpandedUniversePerTickerIdentityAuthorityCandidateReviewPackageError,
        match="per_ticker_identity_review_entries",
    ):
        review.validate_expanded_universe_per_ticker_identity_authority_candidate_review_package_v1(
            package
        )


@pytest.mark.parametrize(
    ("field", "match"),
    [
        ("identity_fields_to_bind", "identity_fields_to_bind"),
        ("identity_field_groups", "identity_field_groups"),
        ("identity_evidence_limitations", "identity_evidence_limitations"),
        ("future_identity_authority_chain", "future_identity_authority_chain"),
        ("future_gates", "future_gates"),
        ("risk_controls", "risk_controls"),
        ("identity_authority_candidate_digest", "identity_authority_candidate_digest"),
    ],
)
def test_validator_rejects_missing_required_review_sections(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    field: str,
    match: str,
):
    package = _package(tmp_path, monkeypatch)
    package.pop(field)

    with pytest.raises(
        review.ExpandedUniversePerTickerIdentityAuthorityCandidateReviewPackageError,
        match=match,
    ):
        review.validate_expanded_universe_per_ticker_identity_authority_candidate_review_package_v1(
            package
        )


def test_validator_rejects_missing_identity_fields(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    package = _package(tmp_path, monkeypatch)
    package["per_ticker_identity_review_entries"][0].pop("identity_fields")

    with pytest.raises(
        review.ExpandedUniversePerTickerIdentityAuthorityCandidateReviewPackageError,
        match="identity fields",
    ):
        review.validate_expanded_universe_per_ticker_identity_authority_candidate_review_package_v1(
            package
        )


def test_validator_rejects_identity_fields_without_value_status_structure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    package = _package(tmp_path, monkeypatch)
    package["per_ticker_identity_review_entries"][0]["identity_fields"]["ticker"] = {
        "value": "MSFT"
    }

    with pytest.raises(
        review.ExpandedUniversePerTickerIdentityAuthorityCandidateReviewPackageError,
        match="value/status",
    ):
        review.validate_expanded_universe_per_ticker_identity_authority_candidate_review_package_v1(
            package
        )


def test_validator_rejects_fabricated_unavailable_fields(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    package = _package(tmp_path, monkeypatch)
    package["per_ticker_identity_review_entries"][0]["identity_fields"]["cik"]["value"] = (
        "123456"
    )

    with pytest.raises(
        review.ExpandedUniversePerTickerIdentityAuthorityCandidateReviewPackageError,
        match="unavailable",
    ):
        review.validate_expanded_universe_per_ticker_identity_authority_candidate_review_package_v1(
            package
        )


def test_validator_rejects_missing_per_ticker_candidate_digest(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    package = _package(tmp_path, monkeypatch)
    package["per_ticker_identity_review_entries"][0].pop(
        "per_ticker_identity_candidate_digest"
    )

    with pytest.raises(
        review.ExpandedUniversePerTickerIdentityAuthorityCandidateReviewPackageError,
        match="per_ticker_identity_candidate_digest",
    ):
        review.validate_expanded_universe_per_ticker_identity_authority_candidate_review_package_v1(
            package
        )


def test_validator_rejects_missing_per_ticker_review_digest(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    package = _package(tmp_path, monkeypatch)
    package["per_ticker_identity_review_entries"][0].pop(
        "per_ticker_identity_review_digest"
    )

    with pytest.raises(
        review.ExpandedUniversePerTickerIdentityAuthorityCandidateReviewPackageError,
        match="per_ticker_identity_review_digest",
    ):
        review.validate_expanded_universe_per_ticker_identity_authority_candidate_review_package_v1(
            package
        )


def test_validator_rejects_review_package_digest_mismatch(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    package = _package(tmp_path, monkeypatch)
    package[
        "expanded_universe_per_ticker_identity_authority_candidate_review_package_digest"
    ] = "0" * 64

    with pytest.raises(
        review.ExpandedUniversePerTickerIdentityAuthorityCandidateReviewPackageError,
        match="expanded_universe_per_ticker_identity_authority_candidate_review_package_digest",
    ):
        review.validate_expanded_universe_per_ticker_identity_authority_candidate_review_package_v1(
            package
        )


def test_markdown_includes_required_sections(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    markdown = review.build_expanded_universe_per_ticker_identity_authority_candidate_review_markdown_v1(
        _package(tmp_path, monkeypatch)
    )

    for section in (
        "## Title",
        "## Reviewed Expanded Universe Identity Authority Candidate",
        "## Source Identity Candidate",
        "## Source Live Ticker Validation Evidence",
        "## Target Universe",
        "## Per-Ticker Identity Review Summary",
        "## Identity Fields Reviewed",
        "## Unavailable Fields and Limitations",
        "## Future Identity Authority Chain",
        "## Future Gates",
        "## Risk Controls",
        "## Authority Boundary",
        "## Acquisition Boundary",
        "## Dataset Boundary",
        "## Predictive/Profitability Boundary",
        "## Runtime Boundary",
        "## Checklist Summary",
        "## Guardrails",
    ):
        assert section in markdown


def test_write_review_package_writes_json_without_overwrite(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    package_candidate = _candidate(tmp_path, monkeypatch)
    output_dir = tmp_path / "out"

    result = review.write_expanded_universe_per_ticker_identity_authority_candidate_review_package_v1(
        output_dir,
        candidate=package_candidate,
    )

    assert result["artifact_kind"] == (
        review.ARTIFACT_KIND_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_CANDIDATE_REVIEW_PACKAGE
    )
    written = json.loads((output_dir / result["filename"]).read_text(encoding="utf-8"))
    assert written["review_status"] == (
        review.EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_READY
    )
    with pytest.raises(
        review.ExpandedUniversePerTickerIdentityAuthorityCandidateReviewPackageError,
        match="already exists",
    ):
        review.write_expanded_universe_per_ticker_identity_authority_candidate_review_package_v1(
            output_dir,
            candidate=package_candidate,
        )


def test_services_package_exports_candidate_review_helpers():
    import marketflow.services as services

    assert services.ARTIFACT_KIND_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_CANDIDATE_REVIEW_PACKAGE == (
        review.ARTIFACT_KIND_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_CANDIDATE_REVIEW_PACKAGE
    )
    assert services.EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_READY == (
        review.EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_READY
    )
    assert services.build_expanded_universe_per_ticker_identity_authority_candidate_review_package_v1 is (
        review.build_expanded_universe_per_ticker_identity_authority_candidate_review_package_v1
    )
    assert services.validate_expanded_universe_per_ticker_identity_authority_candidate_review_package_v1 is (
        review.validate_expanded_universe_per_ticker_identity_authority_candidate_review_package_v1
    )
    assert services.write_expanded_universe_per_ticker_identity_authority_candidate_review_package_v1 is (
        review.write_expanded_universe_per_ticker_identity_authority_candidate_review_package_v1
    )
    assert services.build_expanded_universe_per_ticker_identity_authority_candidate_review_markdown_v1 is (
        review.build_expanded_universe_per_ticker_identity_authority_candidate_review_markdown_v1
    )
    assert services.expanded_universe_per_ticker_identity_authority_candidate_review_package_digest_v1 is (
        review.expanded_universe_per_ticker_identity_authority_candidate_review_package_digest_v1
    )
