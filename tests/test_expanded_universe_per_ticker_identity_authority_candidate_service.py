from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from marketflow.historical_data.artifacts import canonical_json_bytes, sha256_bytes
from marketflow.services import (
    expanded_universe_per_ticker_identity_authority_candidate_service as candidate_service,
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
    root.mkdir()
    tickers = candidate_service.VALIDATION_TARGET_UNIVERSE
    results = [
        {
            "ticker": ticker,
            "live_validation_status": candidate_service.plan_review.plan.VALIDATED_READ_ONLY,
            "active_status": candidate_service.plan_review.plan.VALIDATED_READ_ONLY,
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
    monkeypatch.setattr(candidate_service, "EXPECTED_SOURCE_OUTPUT_DIGESTS", digests)
    return root


def _candidate(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> dict[str, Any]:
    return candidate_service.build_expanded_universe_per_ticker_identity_authority_candidate_v1(
        output_root=_fixture_output_root(tmp_path, monkeypatch)
    )


def _mutated_candidate(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    field: str,
    value: Any,
) -> dict[str, Any]:
    candidate = _candidate(tmp_path, monkeypatch)
    candidate[field] = value
    return candidate


def test_candidate_builds_offline_without_provider_calls(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    def fail_provider_call(*_args, **_kwargs):  # pragma: no cover
        raise AssertionError("provider path must not be called")

    monkeypatch.setattr(
        candidate_service.plan_review.plan.results_review.provider,
        "fetch_massive_ticker_details_v1",
        fail_provider_call,
    )

    candidate = _candidate(tmp_path, monkeypatch)

    assert candidate["created_offline"] is True
    assert candidate["provider_requests_made"] is False
    assert candidate["live_validation_rerun_performed"] is False
    assert candidate["live_provider_transport_enabled"] is False


def test_artifact_kind_and_ready_status_when_fixture_validation_outputs_are_present(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    candidate = _candidate(tmp_path, monkeypatch)

    assert candidate["artifact_kind"] == (
        candidate_service.ARTIFACT_KIND_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_CANDIDATE
    )
    assert candidate["candidate_status"] == (
        candidate_service.EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_READY_FOR_OPERATOR_REVIEW
    )
    assert candidate["schema_version"] == (
        candidate_service.SCHEMA_VERSION_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_CANDIDATE_V1
    )


def test_candidate_status_is_blocked_when_validation_outputs_are_missing(tmp_path: Path):
    candidate = candidate_service.build_expanded_universe_per_ticker_identity_authority_candidate_v1(
        output_root=tmp_path / "missing"
    )

    assert candidate["candidate_status"] == (
        candidate_service.EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_BLOCKED_MISSING_VALIDATION_OUTPUTS
    )
    assert candidate["source_output_file_inspection_performed"] is False
    assert candidate["source_output_digests_verified"] is False
    assert candidate["per_ticker_identity_authority_candidate_created"] is False
    assert candidate["per_ticker_identity_candidate_entries"] == []


def test_source_evidence_digests_are_bound(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    candidate = _candidate(tmp_path, monkeypatch)

    assert candidate["identity_authority_plan_candidate_review_package_digest"] == (
        candidate_service.EXPECTED_IDENTITY_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST
    )
    assert candidate["identity_authority_plan_candidate_digest"] == (
        candidate_service.EXPECTED_IDENTITY_AUTHORITY_PLAN_CANDIDATE_DIGEST
    )
    assert candidate["live_ticker_validation_results_review_package_digest"] == (
        candidate_service.plan_review.plan.EXPECTED_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_DIGEST
    )
    assert candidate["live_ticker_validation_execution_digest"] == (
        candidate_service.plan_review.plan.EXPECTED_LIVE_TICKER_VALIDATION_EXECUTION_DIGEST
    )
    assert candidate["live_ticker_validation_approval_digest"] == (
        candidate_service.plan_review.plan.EXPECTED_LIVE_TICKER_VALIDATION_APPROVAL_DIGEST
    )
    assert candidate["ticker_universe_selection_approval_digest"] == (
        candidate_service.plan_review.plan.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST
    )


def test_source_output_digests_are_verified_for_ready_candidate(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    candidate = _candidate(tmp_path, monkeypatch)

    assert candidate["source_output_digests_verified"] is True
    assert {item["digest_verified"] for item in candidate["source_output_digest_manifest"]} == {
        True
    }


def test_target_universe_and_reviewed_validation_status_are_preserved(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    candidate = _candidate(tmp_path, monkeypatch)

    assert candidate["target_universe_count"] == 12
    assert candidate["target_universe"] == candidate_service.VALIDATION_TARGET_UNIVERSE
    assert candidate["validated_universe"] == candidate_service.VALIDATION_TARGET_UNIVERSE
    assert candidate["all_targets_validated_read_only"] is True
    assert candidate["validated_read_only_count"] == 12
    assert candidate["provider_request_count"] == 12
    assert candidate["successful_provider_response_count"] == 12
    assert candidate["failed_provider_response_count"] == 0
    assert candidate["validation_supports_future_authority_chain_planning"] is True
    assert candidate["validation_creates_new_ticker_authority"] is False
    assert candidate["validation_creates_acquisition_authority"] is False
    assert candidate["validation_creates_dataset_generation_authority"] is False
    assert candidate["validation_creates_predictive_evidence_authority"] is False


def test_candidate_scope_and_per_ticker_entries_are_candidate_only(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    candidate = _candidate(tmp_path, monkeypatch)
    entries = candidate["per_ticker_identity_candidate_entries"]

    assert candidate["identity_authority_candidate_scope"] == (
        candidate_service.CANDIDATE_ONLY_NOT_AUTHORITY
    )
    assert len(entries) == 12
    for entry in entries:
        assert entry["identity_candidate_status"] == (
            candidate_service.IDENTITY_CANDIDATE_READY_FOR_OPERATOR_REVIEW
        )
        assert entry["live_validation_status"] == (
            candidate_service.plan_review.plan.VALIDATED_READ_ONLY
        )
        assert entry["identity_authority_created"] is False
        assert entry["identity_freeze_status"] == candidate_service.plan_review.plan.NOT_FROZEN
        assert entry["identity_review_status"] == candidate_service.plan_review.plan.NOT_CREATED


def test_identity_fields_to_bind_are_defined_and_use_value_status_structure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    candidate = _candidate(tmp_path, monkeypatch)

    assert candidate["identity_fields_to_bind"] == candidate_service.IDENTITY_FIELDS_TO_BIND
    for entry in candidate["per_ticker_identity_candidate_entries"]:
        assert set(entry["identity_fields"]) == set(candidate_service.IDENTITY_FIELDS_TO_BIND)
        for field in entry["identity_fields"].values():
            assert set(field) == {"value", "status"}
            assert field["status"] in {
                candidate_service.AVAILABLE_FROM_SOURCE,
                candidate_service.UNAVAILABLE_IN_SOURCE,
            }


def test_unavailable_fields_are_marked_unavailable_and_not_fabricated(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    candidate = _candidate(tmp_path, monkeypatch)
    unavailable_count = 0

    for entry in candidate["per_ticker_identity_candidate_entries"]:
        for field in entry["identity_fields"].values():
            if field["status"] == candidate_service.UNAVAILABLE_IN_SOURCE:
                unavailable_count += 1
                assert field["value"] is None

    assert unavailable_count > 0


def test_provider_response_and_sanitized_validation_digests_are_bound_or_unavailable(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    candidate = _candidate(tmp_path, monkeypatch)

    for entry in candidate["per_ticker_identity_candidate_entries"]:
        provider_digest = entry["identity_fields"]["provider_response_digest"]
        sanitized_digest = entry["identity_fields"]["sanitized_validation_digest"]
        assert provider_digest["status"] == candidate_service.AVAILABLE_FROM_SOURCE
        assert provider_digest["value"]
        assert sanitized_digest["status"] == candidate_service.AVAILABLE_FROM_SOURCE
        assert sanitized_digest["value"]


def test_per_ticker_identity_candidate_digests_are_present_and_deterministic(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    first = _candidate(tmp_path, monkeypatch)
    second = candidate_service.build_expanded_universe_per_ticker_identity_authority_candidate_v1(
        output_root=Path(first["source_output_root"])
    )

    first_digests = [
        entry["per_ticker_identity_candidate_digest"]
        for entry in first["per_ticker_identity_candidate_entries"]
    ]
    second_digests = [
        entry["per_ticker_identity_candidate_digest"]
        for entry in second["per_ticker_identity_candidate_entries"]
    ]
    assert first_digests == second_digests
    for entry in first["per_ticker_identity_candidate_entries"]:
        assert entry["per_ticker_identity_candidate_digest"] == (
            candidate_service.per_ticker_identity_candidate_digest_v1(entry)
        )


def test_field_classification_limitations_future_chain_gates_and_risk_controls_are_defined(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    candidate = _candidate(tmp_path, monkeypatch)

    assert candidate["identity_field_groups"] == candidate_service.IDENTITY_FIELD_GROUPS
    assert candidate["identity_evidence_limitations"] == (
        candidate_service.IDENTITY_EVIDENCE_LIMITATIONS
    )
    assert candidate["future_identity_authority_chain"] == (
        candidate_service._future_identity_authority_chain()
    )
    assert candidate["future_gates"] == candidate_service.FUTURE_GATES
    assert candidate["risk_controls"] == candidate_service.RISK_CONTROLS


@pytest.mark.parametrize(
    "field",
    [
        "provider_requests_made",
        "live_validation_rerun_performed",
        "live_provider_transport_enabled",
        "per_ticker_identity_authority_review_created",
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
    assert _candidate(tmp_path, monkeypatch)[field] is False


def test_predictive_profitability_and_runtime_authorizations_remain_closed(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    candidate = _candidate(tmp_path, monkeypatch)

    assert candidate["predictive_usefulness"] == (
        candidate_service.acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED
    )
    assert candidate["profitability"] == (
        candidate_service.acquisition.PROFITABILITY_NOT_ACCEPTED
    )
    assert candidate["runtime_use"] == candidate_service.plan_review.plan.NOT_AUTHORIZED
    assert candidate["strategy_use"] == candidate_service.plan_review.plan.NOT_AUTHORIZED
    assert candidate["paper_trading"] == candidate_service.plan_review.plan.NOT_AUTHORIZED
    assert candidate["broker_execution"] == candidate_service.plan_review.plan.NOT_AUTHORIZED
    assert candidate["candidate_summary"]["ready_for_identity_freeze"] is False


def test_checklist_contains_all_required_check_ids_and_all_pass_for_ready_candidate(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    candidate = _candidate(tmp_path, monkeypatch)

    assert [item["check_id"] for item in candidate["candidate_checklist"]] == (
        candidate_service.REQUIRED_CHECK_IDS
    )
    assert {item["status"] for item in candidate["candidate_checklist"]} == {
        candidate_service.PASS
    }


def test_summary_counts_total_passed_failed_and_blockers_correctly(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    candidate = _candidate(tmp_path, monkeypatch)
    summary = candidate["candidate_summary"]

    assert summary["total_checks"] == len(candidate_service.REQUIRED_CHECK_IDS)
    assert summary["passed_checks"] == len(candidate_service.REQUIRED_CHECK_IDS)
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["ready_for_operator_review"] is True
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


def test_candidate_digest_is_deterministic(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    first = _candidate(tmp_path, monkeypatch)
    second = candidate_service.build_expanded_universe_per_ticker_identity_authority_candidate_v1(
        output_root=Path(first["source_output_root"])
    )

    assert first["expanded_universe_per_ticker_identity_authority_candidate_digest"] == (
        second["expanded_universe_per_ticker_identity_authority_candidate_digest"]
    )
    assert first["expanded_universe_per_ticker_identity_authority_candidate_digest"] == (
        candidate_service.expanded_universe_per_ticker_identity_authority_candidate_digest_v1(
            first
        )
    )


def test_validator_accepts_valid_candidate(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    validation = candidate_service.validate_expanded_universe_per_ticker_identity_authority_candidate_v1(
        _candidate(tmp_path, monkeypatch)
    )

    assert validation["status"] == (
        "EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_CANDIDATE_VALID"
    )
    assert validation["ready_for_operator_review"] is True
    assert validation["ready_for_identity_freeze"] is False


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("artifact_kind", "EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_FROZEN", "artifact_kind"),
        ("provider_requests_made", True, "provider_requests_made"),
        ("live_validation_rerun_performed", True, "live_validation_rerun_performed"),
        ("live_provider_transport_enabled", True, "live_provider_transport_enabled"),
        ("target_universe_count", 11, "target_universe_count"),
        ("identity_authority_created", True, "identity_authority_created"),
        ("per_ticker_identity_authority_review_created", True, "per_ticker_identity_authority_review_created"),
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
    candidate = _mutated_candidate(tmp_path, monkeypatch, field, value)

    with pytest.raises(
        candidate_service.ExpandedUniversePerTickerIdentityAuthorityCandidateError,
        match=match,
    ):
        candidate_service.validate_expanded_universe_per_ticker_identity_authority_candidate_v1(
            candidate
        )


def test_validator_rejects_status_ready_while_source_outputs_are_missing(
    tmp_path: Path,
):
    candidate = candidate_service.build_expanded_universe_per_ticker_identity_authority_candidate_v1(
        output_root=tmp_path / "missing"
    )
    candidate["candidate_status"] = (
        candidate_service.EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_READY_FOR_OPERATOR_REVIEW
    )

    with pytest.raises(
        candidate_service.ExpandedUniversePerTickerIdentityAuthorityCandidateError,
        match="source outputs",
    ):
        candidate_service.validate_expanded_universe_per_ticker_identity_authority_candidate_v1(
            candidate
        )


def test_validator_rejects_target_universe_mismatch(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    candidate = _candidate(tmp_path, monkeypatch)
    candidate["target_universe"] = candidate["target_universe"][:-1]

    with pytest.raises(
        candidate_service.ExpandedUniversePerTickerIdentityAuthorityCandidateError,
        match="target_universe|target universe",
    ):
        candidate_service.validate_expanded_universe_per_ticker_identity_authority_candidate_v1(
            candidate
        )


def test_validator_rejects_non_validated_read_only_target(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    candidate = _candidate(tmp_path, monkeypatch)
    candidate["per_ticker_identity_candidate_entries"][0]["live_validation_status"] = "FAILED"

    with pytest.raises(
        candidate_service.ExpandedUniversePerTickerIdentityAuthorityCandidateError,
        match="live_validation_status",
    ):
        candidate_service.validate_expanded_universe_per_ticker_identity_authority_candidate_v1(
            candidate
        )


def test_validator_rejects_per_ticker_candidate_count_not_12(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    candidate = _candidate(tmp_path, monkeypatch)
    candidate["per_ticker_identity_candidate_entries"] = (
        candidate["per_ticker_identity_candidate_entries"][:-1]
    )

    with pytest.raises(
        candidate_service.ExpandedUniversePerTickerIdentityAuthorityCandidateError,
        match="per_ticker_identity_candidate_entries",
    ):
        candidate_service.validate_expanded_universe_per_ticker_identity_authority_candidate_v1(
            candidate
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
        ("identity_authority_plan_candidate_review_package_digest", "identity_authority_plan_candidate_review_package_digest"),
        ("live_ticker_validation_results_review_package_digest", "live_ticker_validation_results_review_package_digest"),
    ],
)
def test_validator_rejects_missing_required_candidate_sections(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    field: str,
    match: str,
):
    candidate = _candidate(tmp_path, monkeypatch)
    candidate.pop(field)

    with pytest.raises(
        candidate_service.ExpandedUniversePerTickerIdentityAuthorityCandidateError,
        match=match,
    ):
        candidate_service.validate_expanded_universe_per_ticker_identity_authority_candidate_v1(
            candidate
        )


def test_validator_rejects_missing_identity_fields(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    candidate = _candidate(tmp_path, monkeypatch)
    candidate["per_ticker_identity_candidate_entries"][0].pop("identity_fields")

    with pytest.raises(
        candidate_service.ExpandedUniversePerTickerIdentityAuthorityCandidateError,
        match="identity fields",
    ):
        candidate_service.validate_expanded_universe_per_ticker_identity_authority_candidate_v1(
            candidate
        )


def test_validator_rejects_identity_fields_without_value_status_structure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    candidate = _candidate(tmp_path, monkeypatch)
    candidate["per_ticker_identity_candidate_entries"][0]["identity_fields"]["ticker"] = {
        "value": "MSFT"
    }

    with pytest.raises(
        candidate_service.ExpandedUniversePerTickerIdentityAuthorityCandidateError,
        match="value/status",
    ):
        candidate_service.validate_expanded_universe_per_ticker_identity_authority_candidate_v1(
            candidate
        )


def test_validator_rejects_fabricated_unavailable_fields(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    candidate = _candidate(tmp_path, monkeypatch)
    candidate["per_ticker_identity_candidate_entries"][0]["identity_fields"][
        "cik"
    ]["value"] = "123456"

    with pytest.raises(
        candidate_service.ExpandedUniversePerTickerIdentityAuthorityCandidateError,
        match="unavailable",
    ):
        candidate_service.validate_expanded_universe_per_ticker_identity_authority_candidate_v1(
            candidate
        )


def test_validator_rejects_missing_per_ticker_candidate_digest(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    candidate = _candidate(tmp_path, monkeypatch)
    candidate["per_ticker_identity_candidate_entries"][0].pop(
        "per_ticker_identity_candidate_digest"
    )

    with pytest.raises(
        candidate_service.ExpandedUniversePerTickerIdentityAuthorityCandidateError,
        match="per_ticker_identity_candidate_digest",
    ):
        candidate_service.validate_expanded_universe_per_ticker_identity_authority_candidate_v1(
            candidate
        )


def test_validator_rejects_candidate_digest_mismatch(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    candidate = _candidate(tmp_path, monkeypatch)
    candidate["expanded_universe_per_ticker_identity_authority_candidate_digest"] = (
        "0" * 64
    )

    with pytest.raises(
        candidate_service.ExpandedUniversePerTickerIdentityAuthorityCandidateError,
        match="expanded_universe_per_ticker_identity_authority_candidate_digest",
    ):
        candidate_service.validate_expanded_universe_per_ticker_identity_authority_candidate_v1(
            candidate
        )


def test_markdown_includes_required_sections(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    markdown = candidate_service.build_expanded_universe_per_ticker_identity_authority_candidate_markdown_v1(
        _candidate(tmp_path, monkeypatch)
    )

    for section in (
        "## Title",
        "## Purpose",
        "## Source Live Ticker Validation Evidence",
        "## Target Universe",
        "## Per-Ticker Identity Candidate Summary",
        "## Identity Fields to Bind",
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


def test_write_candidate_writes_json_without_overwrite(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    source_root = _fixture_output_root(tmp_path, monkeypatch)
    output_dir = tmp_path / "out"

    result = candidate_service.write_expanded_universe_per_ticker_identity_authority_candidate_v1(
        output_dir,
        output_root=source_root,
    )

    assert result["artifact_kind"] == (
        candidate_service.ARTIFACT_KIND_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_CANDIDATE
    )
    written = json.loads((output_dir / result["filename"]).read_text(encoding="utf-8"))
    assert written["candidate_status"] == (
        candidate_service.EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_READY_FOR_OPERATOR_REVIEW
    )
    with pytest.raises(
        candidate_service.ExpandedUniversePerTickerIdentityAuthorityCandidateError,
        match="already exists",
    ):
        candidate_service.write_expanded_universe_per_ticker_identity_authority_candidate_v1(
            output_dir,
            output_root=source_root,
        )


def test_services_package_exports_identity_authority_candidate_helpers():
    import marketflow.services as services

    assert services.ARTIFACT_KIND_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_CANDIDATE == (
        candidate_service.ARTIFACT_KIND_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_CANDIDATE
    )
    assert services.EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_READY_FOR_OPERATOR_REVIEW == (
        candidate_service.EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_READY_FOR_OPERATOR_REVIEW
    )
    assert services.build_expanded_universe_per_ticker_identity_authority_candidate_v1 is (
        candidate_service.build_expanded_universe_per_ticker_identity_authority_candidate_v1
    )
    assert services.validate_expanded_universe_per_ticker_identity_authority_candidate_v1 is (
        candidate_service.validate_expanded_universe_per_ticker_identity_authority_candidate_v1
    )
    assert services.write_expanded_universe_per_ticker_identity_authority_candidate_v1 is (
        candidate_service.write_expanded_universe_per_ticker_identity_authority_candidate_v1
    )
    assert services.build_expanded_universe_per_ticker_identity_authority_candidate_markdown_v1 is (
        candidate_service.build_expanded_universe_per_ticker_identity_authority_candidate_markdown_v1
    )
    assert services.expanded_universe_per_ticker_identity_authority_candidate_digest_v1 is (
        candidate_service.expanded_universe_per_ticker_identity_authority_candidate_digest_v1
    )
