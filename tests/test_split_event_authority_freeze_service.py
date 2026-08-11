from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest

from marketflow import services
from marketflow.services import split_event_authority_freeze_service as freeze


def _source_review_package() -> dict[str, Any]:
    return {
        "artifact_kind": freeze.review.ARTIFACT_KIND_SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE,
        "review_status": freeze.review.SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_READY,
        "split_event_evidence_results_review_package_digest": (
            freeze.EXPECTED_SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST
        ),
        "source_split_provider_evidence_execution_digest": (
            freeze.EXPECTED_SPLIT_PROVIDER_EVIDENCE_EXECUTION_DIGEST
        ),
        "split_provider_evidence_request_approval_digest": (
            freeze.EXPECTED_SPLIT_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST
        ),
        "split_event_authority_candidate_review_package_digest": (
            freeze.EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "split_event_authority_candidate_digest": (
            freeze.EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_DIGEST
        ),
        "dividend_event_authority_candidate_review_package_digest": (
            freeze.EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "dividend_event_authority_candidate_digest": (
            freeze.EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_DIGEST
        ),
        "corporate_action_authority_plan_approval_digest": (
            freeze.EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST
        ),
        "post_identity_freeze_registry_inventory_approval_digest": (
            freeze.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST
        ),
        "identity_authority_freeze_digest": freeze.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
        "target_universe": freeze.TARGET_UNIVERSE,
        "target_universe_count": 12,
        "provider_request_count": 12,
        "successful_provider_response_count": 12,
        "failed_provider_response_count": 0,
        "split_evidence_collected_count": 7,
        "no_split_events_returned_count": 5,
        "failure_count": 0,
        "warning_count": 12,
        "provider_requests_made_in_review": False,
        "split_provider_evidence_rerun_performed": False,
        "live_provider_transport_enabled_in_review": False,
        "review_summary": {
            "total_checks": 69,
            "passed_checks": 69,
            "failed_checks": 0,
            "blocker_count": 0,
        },
        "per_ticker_split_evidence_summary": [
            {
                "ticker": ticker,
                "split_provider_evidence_status": freeze.review.EXPECTED_PER_TICKER_STATUS[
                    ticker
                ],
            }
            for ticker in freeze.TARGET_UNIVERSE
        ],
    }


def _attestation(**overrides: Any) -> dict[str, Any]:
    payload = {
        "operator_reference": "TEST_OPERATOR",
        "operator_attestation_timestamp_utc": "2026-08-11T00:00:00Z",
        "operator_attestation_phrase": (
            freeze.REQUIRED_SPLIT_EVENT_AUTHORITY_FREEZE_ATTESTATION_PHRASE
        ),
        "operator_confirms_split_evidence_results_review_package_digest": (
            freeze.EXPECTED_SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST
        ),
        "operator_confirms_split_provider_evidence_execution_digest": (
            freeze.EXPECTED_SPLIT_PROVIDER_EVIDENCE_EXECUTION_DIGEST
        ),
        "operator_confirms_split_provider_evidence_request_approval_digest": (
            freeze.EXPECTED_SPLIT_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST
        ),
        "operator_confirms_split_candidate_review_package_digest": (
            freeze.EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "operator_confirms_split_candidate_digest": (
            freeze.EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_DIGEST
        ),
        "operator_confirms_dividend_candidate_review_package_digest": (
            freeze.EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "operator_confirms_corporate_action_plan_approval_digest": (
            freeze.EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST
        ),
        "operator_confirms_registry_inventory_approval_digest": (
            freeze.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST
        ),
        "operator_confirms_identity_freeze_digest": (
            freeze.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST
        ),
        "operator_confirms_target_universe": freeze.TARGET_UNIVERSE,
        "operator_confirms_target_count": 12,
        "operator_confirms_authority_scope_split_event_only": True,
        "operator_confirms_split_evidence_collected_count": 7,
        "operator_confirms_no_split_events_returned_count": 5,
        "operator_confirms_no_split_authority_provider_rerun": True,
        "operator_confirms_no_provider_requests_in_freeze": True,
        "operator_confirms_no_live_provider_transport_enabled": True,
        "operator_confirms_no_dividend_provider_evidence_request_authorized": True,
        "operator_confirms_no_dividend_event_authority_created": True,
        "operator_confirms_no_corporate_action_authority_created": True,
        "operator_confirms_no_acquisition_authority": True,
        "operator_confirms_no_dataset_generation_authorization": True,
        "operator_confirms_no_predictive_usefulness_acceptance": True,
        "operator_confirms_no_profitability_acceptance": True,
        "operator_confirms_no_runtime_migration_approval": True,
        "operator_confirms_no_runtime_activation": True,
        "operator_confirms_no_paper_trading": True,
        "operator_confirms_no_broker_execution": True,
        "operator_confirms_no_trade_recommendations": True,
        "operator_confirms_no_api_key_storage_or_printing": True,
        "operator_confirms_no_raw_payload_commit": True,
    }
    payload.update(overrides)
    return freeze.build_split_event_authority_freeze_attestation_v1(**payload)


def _package(**attestation_overrides: Any) -> dict[str, Any]:
    return freeze.build_split_event_authority_frozen_v1(
        split_evidence_results_review_package=_source_review_package(),
        operator_attestation=_attestation(**attestation_overrides),
    )


def test_operator_attestation_builder_creates_required_fields():
    attestation = _attestation()

    assert attestation["operator_decision"] == freeze.OPERATOR_DECISION_FREEZE_SPLIT_EVENT_AUTHORITY
    assert attestation["operator_attestation_phrase"] == (
        freeze.REQUIRED_SPLIT_EVENT_AUTHORITY_FREEZE_ATTESTATION_PHRASE
    )
    assert attestation["operator_attestation_version"] == (
        freeze.OPERATOR_ATTESTATION_VERSION_SPLIT_EVENT_AUTHORITY_FREEZE_V1
    )
    assert attestation["operator_reference"] == "TEST_OPERATOR"
    assert attestation["operator_confirms_target_universe"] == freeze.TARGET_UNIVERSE
    assert all(
        attestation[field] is True
        for field in freeze.REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS
    )


def test_frozen_artifact_builds_offline_without_provider_calls(monkeypatch: pytest.MonkeyPatch):
    def fail_review_build(*_args: Any, **_kwargs: Any) -> None:  # pragma: no cover
        raise AssertionError("review package should be supplied by offline test fixture")

    monkeypatch.setattr(
        freeze.review,
        "build_split_event_evidence_results_review_package_v1",
        fail_review_build,
    )
    package = _package()

    assert package["created_offline"] is True
    assert package["provider_requests_made_in_freeze"] is False
    assert package["live_provider_transport_enabled_in_freeze"] is False
    assert package["split_provider_evidence_rerun_performed"] is False


def test_artifact_kind_status_scope_and_freeze_state_are_exact():
    package = _package()

    assert package["artifact_kind"] == freeze.ARTIFACT_KIND_SPLIT_EVENT_AUTHORITY_FROZEN
    assert package["freeze_status"] == freeze.SPLIT_EVENT_AUTHORITY_FROZEN
    assert package["authority_scope"] == freeze.SPLIT_EVENT_AUTHORITY_ONLY
    assert package["split_event_authority_created"] is True
    assert package["split_event_authority_frozen"] is True


def test_source_evidence_digests_and_target_universe_are_bound():
    package = _package()

    assert package["split_event_evidence_results_review_package_digest"] == (
        freeze.EXPECTED_SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST
    )
    assert package["split_provider_evidence_execution_digest"] == (
        freeze.EXPECTED_SPLIT_PROVIDER_EVIDENCE_EXECUTION_DIGEST
    )
    assert package["split_provider_evidence_request_approval_digest"] == (
        freeze.EXPECTED_SPLIT_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST
    )
    assert package["split_event_authority_candidate_review_package_digest"] == (
        freeze.EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST
    )
    assert package["split_event_authority_candidate_digest"] == (
        freeze.EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_DIGEST
    )
    assert package["dividend_event_authority_candidate_review_package_digest"] == (
        freeze.EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST
    )
    assert package["corporate_action_authority_plan_approval_digest"] == (
        freeze.EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST
    )
    assert package["post_identity_freeze_registry_inventory_approval_digest"] == (
        freeze.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST
    )
    assert package["identity_authority_freeze_digest"] == (
        freeze.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST
    )
    assert package["target_universe"] == freeze.TARGET_UNIVERSE
    assert package["target_universe_count"] == 12


def test_per_ticker_authority_entries_preserve_classification_and_boundaries():
    package = _package()
    entries = package["per_ticker_split_event_authority"]

    assert len(entries) == 12
    assert [entry["ticker"] for entry in entries] == freeze.TARGET_UNIVERSE
    for entry in entries:
        ticker = entry["ticker"]
        assert entry["split_event_authority_status"] == "FROZEN"
        assert entry["split_event_authority_scope"] == freeze.SPLIT_EVENT_AUTHORITY_ONLY
        assert entry["split_event_authority_classification"] == (
            freeze.PER_TICKER_SPLIT_AUTHORITY_CLASSIFICATION[ticker]
        )
        assert entry["split_provider_evidence_status"] == (
            freeze.review.EXPECTED_PER_TICKER_STATUS[ticker]
        )
        if entry["split_provider_evidence_status"] == (
            freeze.review.execution.NO_SPLIT_EVENTS_RETURNED_BY_PROVIDER
        ):
            assert entry["split_absence_policy_status"] == (
                freeze.APPLIED_IF_NO_SPLIT_EVENTS_RETURNED
            )
        assert len(entry["per_ticker_split_event_authority_freeze_digest"]) == 64
        assert entry["dividend_event_authority_status"] == "NOT_CREATED"
        assert entry["corporate_action_authority_created"] is False
        assert entry["acquisition_authorized"] is False
        assert entry["dataset_generation_authorized"] is False
        assert entry["runtime_use"] == freeze.NOT_AUTHORIZED
        assert entry["strategy_use"] == freeze.NOT_AUTHORIZED
        assert entry["paper_trading"] == freeze.NOT_AUTHORIZED
        assert entry["broker_execution"] == freeze.NOT_AUTHORIZED


def test_split_evidence_counts_checklist_summary_and_remaining_roadmap():
    package = _package()

    assert package["provider_request_count"] == 12
    assert package["successful_provider_response_count"] == 12
    assert package["failed_provider_response_count"] == 0
    assert package["split_evidence_collected_count"] == 7
    assert package["no_split_events_returned_count"] == 5
    assert package["failure_count"] == 0
    assert package["warning_count"] == 12
    assert [item["check_id"] for item in package["freeze_checklist"]] == (
        freeze.REQUIRED_FREEZE_CHECK_IDS
    )
    assert all(item["status"] == freeze.PASS for item in package["freeze_checklist"])
    assert package["freeze_summary"]["total_checks"] == len(freeze.REQUIRED_FREEZE_CHECK_IDS)
    assert package["freeze_summary"]["failed_checks"] == 0
    assert package["freeze_summary"]["blocker_count"] == 0
    assert package["freeze_summary"]["ready_for_dividend_provider_evidence_request_approval"] is True
    assert package["remaining_required_tasks"] == freeze.REMAINING_REQUIRED_TASKS


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("dividend_provider_evidence_request_authorized", False),
        ("dividend_provider_evidence_executed", False),
        ("dividend_event_authority_created", False),
        ("dividend_event_authority_frozen", False),
        ("corporate_action_authority_created", False),
        ("new_ticker_acquisition_authorized", False),
        ("dataset_generation_authorized", False),
        ("acquisition_generation_authorized", False),
        ("canonical_dataset_authorized", False),
        ("registry_approval_created", False),
        ("additional_predictive_evidence_execution_authorized", False),
        ("additional_predictive_evidence_executed", False),
        ("predictive_experiment_rerun_authorized", False),
        ("predictive_experiment_rerun_performed", False),
        ("new_strategy_scoring_performed", False),
        ("trade_recommendations_generated", False),
        ("runtime_migration_approved", False),
        ("runtime_migration_active", False),
        ("automatic_stitching", False),
        ("predictive_usefulness", freeze.NOT_ACCEPTED),
        ("profitability", freeze.PROFITABILITY_NOT_ACCEPTED),
        ("runtime_use", freeze.NOT_AUTHORIZED),
        ("strategy_use", freeze.NOT_AUTHORIZED),
        ("paper_trading", freeze.NOT_AUTHORIZED),
        ("broker_execution", freeze.NOT_AUTHORIZED),
    ],
)
def test_dividend_corporate_acquisition_dataset_predictive_runtime_boundaries_remain_closed(
    field: str, expected: Any
):
    package = _package()

    assert package[field] == expected


@pytest.mark.parametrize(
    "override",
    [
        {"operator_decision": "APPROVE_SOMETHING_ELSE"},
        {"operator_attestation_phrase": "wrong"},
        {"operator_confirms_split_evidence_results_review_package_digest": "0" * 64},
        {"operator_confirms_split_provider_evidence_execution_digest": "0" * 64},
        {"operator_confirms_split_provider_evidence_request_approval_digest": "0" * 64},
        {"operator_confirms_split_candidate_review_package_digest": "0" * 64},
        {"operator_confirms_split_candidate_digest": "0" * 64},
        {"operator_confirms_dividend_candidate_review_package_digest": "0" * 64},
        {"operator_confirms_corporate_action_plan_approval_digest": "0" * 64},
        {"operator_confirms_registry_inventory_approval_digest": "0" * 64},
        {"operator_confirms_identity_freeze_digest": "0" * 64},
        {"operator_confirms_target_universe": list(reversed(freeze.TARGET_UNIVERSE))},
        {"operator_confirms_target_count": 11},
        {"operator_confirms_split_evidence_collected_count": 6},
        {"operator_confirms_no_split_events_returned_count": 4},
        {"operator_confirms_authority_scope_split_event_only": False},
        {"operator_confirms_no_split_authority_provider_rerun": False},
        {"operator_confirms_no_provider_requests_in_freeze": False},
        {"operator_confirms_no_live_provider_transport_enabled": False},
        {"operator_confirms_no_dividend_provider_evidence_request_authorized": False},
        {"operator_confirms_no_dividend_event_authority_created": False},
        {"operator_confirms_no_corporate_action_authority_created": False},
        {"operator_confirms_no_acquisition_authority": False},
        {"operator_confirms_no_dataset_generation_authorization": False},
        {"operator_confirms_no_predictive_usefulness_acceptance": False},
        {"operator_confirms_no_profitability_acceptance": False},
        {"operator_confirms_no_runtime_migration_approval": False},
        {"operator_confirms_no_runtime_activation": False},
        {"operator_confirms_no_paper_trading": False},
        {"operator_confirms_no_broker_execution": False},
        {"operator_confirms_no_trade_recommendations": False},
        {"operator_confirms_no_api_key_storage_or_printing": False},
        {"operator_confirms_no_raw_payload_commit": False},
    ],
)
def test_bad_operator_attestation_inputs_are_rejected(override: dict[str, Any]):
    with pytest.raises(freeze.SplitEventAuthorityFreezeError):
        _package(**override)


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("artifact_kind", "WRONG"),
        ("freeze_status", "WRONG"),
        ("authority_scope", "WRONG"),
        ("split_event_authority_created", False),
        ("split_event_authority_frozen", False),
        ("target_universe_count", 11),
        ("target_universe", list(reversed(freeze.TARGET_UNIVERSE))),
        ("split_evidence_collected_count", 6),
        ("no_split_events_returned_count", 4),
        ("provider_requests_made_in_freeze", True),
        ("live_provider_transport_enabled_in_freeze", True),
        ("split_provider_evidence_rerun_performed", True),
        ("dividend_provider_evidence_request_authorized", True),
        ("dividend_provider_evidence_executed", True),
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
        ("predictive_usefulness", "accepted"),
        ("profitability", "accepted"),
        ("runtime_migration_approved", True),
        ("runtime_use", "AUTHORIZED"),
        ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
        ("automatic_stitching", True),
    ],
)
def test_validator_rejects_wrong_artifact_fields(field: str, bad_value: Any):
    package = _package()
    package[field] = bad_value

    with pytest.raises(freeze.SplitEventAuthorityFreezeError):
        freeze.validate_split_event_authority_frozen_v1(package)


def test_validator_rejects_missing_per_ticker_entry_and_digest():
    package = _package()
    package["per_ticker_split_event_authority"] = package[
        "per_ticker_split_event_authority"
    ][:-1]

    with pytest.raises(freeze.SplitEventAuthorityFreezeError):
        freeze.validate_split_event_authority_frozen_v1(package)

    package = _package()
    del package["per_ticker_split_event_authority"][0][
        "per_ticker_split_event_authority_freeze_digest"
    ]
    with pytest.raises(freeze.SplitEventAuthorityFreezeError):
        freeze.validate_split_event_authority_frozen_v1(package)


def test_validator_rejects_missing_freeze_digest():
    package = _package()
    del package["split_event_authority_freeze_digest"]

    with pytest.raises(freeze.SplitEventAuthorityFreezeError):
        freeze.validate_split_event_authority_frozen_v1(package)


def test_freeze_and_per_ticker_digests_are_deterministic():
    first = _package()
    second = _package()

    assert first["split_event_authority_freeze_digest"] == (
        second["split_event_authority_freeze_digest"]
    )
    assert [
        item["per_ticker_split_event_authority_freeze_digest"]
        for item in first["per_ticker_split_event_authority"]
    ] == [
        item["per_ticker_split_event_authority_freeze_digest"]
        for item in second["per_ticker_split_event_authority"]
    ]


def test_markdown_includes_required_sections_and_guardrails():
    markdown = freeze.build_split_event_authority_frozen_markdown_v1(_package())

    for heading in [
        "## Frozen Split Event Authority",
        "## Operator Attestation",
        "## Source Split Evidence Results Review",
        "## Source Split Provider Evidence Execution",
        "## Target Universe",
        "## Frozen Per-Ticker Split Authority Summary",
        "## No-Split Event Absence Policy",
        "## Authority Scope",
        "## Dividend Boundary",
        "## Corporate-Action Authority Boundary",
        "## Acquisition Boundary",
        "## Dataset Boundary",
        "## Predictive/Profitability Boundary",
        "## Runtime Boundary",
        "## Freeze Checklist Summary",
        "## Remaining Required Tasks",
        "## Guardrails",
    ]:
        assert heading in markdown
    assert "No provider request was made in this freeze." in markdown
    assert "No live provider transport was enabled in this freeze." in markdown


def test_writer_writes_json_and_markdown_without_overwrite(tmp_path: Path):
    result = freeze.write_split_event_authority_frozen_v1(
        tmp_path,
        split_evidence_results_review_package=_source_review_package(),
        operator_attestation=_attestation(),
    )

    assert Path(result["json_path"]).is_file()
    assert Path(result["markdown_path"]).is_file()
    assert result["validation"]["status"] == "SPLIT_EVENT_AUTHORITY_FROZEN_VALID"
    with pytest.raises(freeze.SplitEventAuthorityFreezeError):
        freeze.write_split_event_authority_frozen_v1(
            tmp_path,
            split_evidence_results_review_package=_source_review_package(),
            operator_attestation=_attestation(),
        )


def test_public_exports_are_available():
    assert services.ARTIFACT_KIND_SPLIT_EVENT_AUTHORITY_FROZEN == (
        freeze.ARTIFACT_KIND_SPLIT_EVENT_AUTHORITY_FROZEN
    )
    assert services.SPLIT_EVENT_AUTHORITY_FROZEN == freeze.SPLIT_EVENT_AUTHORITY_FROZEN
    assert services.SPLIT_EVENT_AUTHORITY_ONLY == freeze.SPLIT_EVENT_AUTHORITY_ONLY
    assert services.build_split_event_authority_frozen_v1 is (
        freeze.build_split_event_authority_frozen_v1
    )
