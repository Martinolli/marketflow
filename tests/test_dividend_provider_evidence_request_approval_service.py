from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from marketflow import services
from marketflow.services import dividend_provider_evidence_request_approval_service as approval


def _dividend_review_package() -> dict[str, Any]:
    return approval.dividend_review.build_dividend_event_authority_candidate_review_package_v1()


def _split_freeze_artifact() -> dict[str, Any]:
    return {
        "artifact_kind": approval.split_freeze.ARTIFACT_KIND_SPLIT_EVENT_AUTHORITY_FROZEN,
        "freeze_status": approval.split_freeze.SPLIT_EVENT_AUTHORITY_FROZEN,
        "authority_scope": approval.split_freeze.SPLIT_EVENT_AUTHORITY_ONLY,
        "split_event_authority_freeze_digest": approval.EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST,
        "split_event_evidence_results_review_package_digest": (
            approval.EXPECTED_SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST
        ),
        "split_provider_evidence_execution_digest": (
            approval.EXPECTED_SPLIT_PROVIDER_EVIDENCE_EXECUTION_DIGEST
        ),
        "split_provider_evidence_request_approval_digest": (
            approval.EXPECTED_SPLIT_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST
        ),
        "split_event_authority_candidate_review_package_digest": (
            approval.EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "split_event_authority_candidate_digest": (
            approval.EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_DIGEST
        ),
        "split_event_authority_created": True,
        "split_event_authority_frozen": True,
        "split_provider_evidence_rerun_performed": False,
        "target_universe": approval.TARGET_UNIVERSE,
        "target_universe_count": 12,
    }


def _attestation(**overrides: Any) -> dict[str, Any]:
    payload = {
        "operator_reference": "TEST_OPERATOR",
        "operator_attestation_timestamp_utc": "2026-08-12T00:00:00Z",
        "operator_attestation_phrase": (
            approval.REQUIRED_DIVIDEND_PROVIDER_EVIDENCE_REQUEST_APPROVAL_ATTESTATION_PHRASE
        ),
        "operator_confirms_dividend_candidate_review_package_digest": (
            approval.EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "operator_confirms_dividend_candidate_digest": (
            approval.EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_DIGEST
        ),
        "operator_confirms_split_event_authority_freeze_digest": (
            approval.EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST
        ),
        "operator_confirms_split_evidence_results_review_package_digest": (
            approval.EXPECTED_SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST
        ),
        "operator_confirms_corporate_action_plan_approval_digest": (
            approval.EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST
        ),
        "operator_confirms_registry_inventory_approval_digest": (
            approval.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST
        ),
        "operator_confirms_identity_freeze_digest": (
            approval.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST
        ),
        "operator_confirms_target_universe": approval.TARGET_UNIVERSE,
        "operator_confirms_target_count": 12,
        "operator_confirms_request_scope_read_only_dividend_event_evidence_only": True,
        "operator_confirms_ready_for_dividend_provider_evidence_execution": True,
        "operator_confirms_no_provider_requests_made_in_approval": True,
        "operator_confirms_no_live_provider_transport_enabled": True,
        "operator_confirms_no_dividend_provider_evidence_executed": True,
        "operator_confirms_no_dividend_provider_evidence_results_created": True,
        "operator_confirms_no_dividend_event_authority_created": True,
        "operator_confirms_no_dividend_event_authority_frozen": True,
        "operator_confirms_split_event_authority_frozen": True,
        "operator_confirms_no_split_provider_evidence_rerun": True,
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
    return approval.build_dividend_provider_evidence_request_approval_attestation_v1(
        **payload
    )


def _package(**attestation_overrides: Any) -> dict[str, Any]:
    return approval.build_dividend_provider_evidence_request_approved_v1(
        dividend_candidate_review_package=_dividend_review_package(),
        split_authority_freeze_artifact=_split_freeze_artifact(),
        operator_attestation=_attestation(**attestation_overrides),
    )


def test_operator_attestation_builder_creates_required_fields():
    attestation = _attestation()

    assert attestation["operator_decision"] == (
        approval.OPERATOR_DECISION_APPROVE_DIVIDEND_PROVIDER_EVIDENCE_REQUEST
    )
    assert attestation["operator_attestation_phrase"] == (
        approval.REQUIRED_DIVIDEND_PROVIDER_EVIDENCE_REQUEST_APPROVAL_ATTESTATION_PHRASE
    )
    assert attestation["operator_attestation_version"] == (
        approval.OPERATOR_ATTESTATION_VERSION_DIVIDEND_PROVIDER_EVIDENCE_REQUEST_APPROVAL_V1
    )
    assert attestation["operator_reference"] == "TEST_OPERATOR"
    assert attestation["operator_confirms_target_universe"] == approval.TARGET_UNIVERSE
    assert all(
        attestation[field] is True
        for field in approval.REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS
    )


def test_approval_artifact_builds_offline_without_provider_calls(
    monkeypatch: pytest.MonkeyPatch,
):
    source_review = _dividend_review_package()
    source_split_freeze = _split_freeze_artifact()

    monkeypatch.setattr(
        approval.dividend_review,
        "build_dividend_event_authority_candidate_review_package_v1",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(
            AssertionError("dividend review source must be supplied")
        ),
    )
    package = approval.build_dividend_provider_evidence_request_approved_v1(
        dividend_candidate_review_package=source_review,
        split_authority_freeze_artifact=source_split_freeze,
        operator_attestation=_attestation(),
    )

    assert package["created_offline"] is True
    assert package["provider_requests_made_in_approval"] is False
    assert package["live_provider_transport_enabled_in_approval"] is False
    assert package["dividend_provider_evidence_executed"] is False


def test_artifact_kind_status_scope_and_request_authorization_are_exact():
    package = _package()

    assert package["artifact_kind"] == (
        approval.ARTIFACT_KIND_DIVIDEND_PROVIDER_EVIDENCE_REQUEST_APPROVED
    )
    assert package["approval_status"] == approval.DIVIDEND_PROVIDER_EVIDENCE_REQUEST_APPROVED
    assert package["approval_scope"] == (
        approval.READ_ONLY_DIVIDEND_EVENT_EVIDENCE_REQUEST_APPROVAL_ONLY
    )
    assert package["dividend_provider_evidence_request_authorized"] is True
    assert package["ready_for_dividend_provider_evidence_execution"] is True


def test_source_digests_and_target_universe_are_bound():
    package = _package()

    assert package["dividend_event_authority_candidate_review_package_digest"] == (
        approval.EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST
    )
    assert package["dividend_event_authority_candidate_digest"] == (
        approval.EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_DIGEST
    )
    assert package["split_event_authority_freeze_digest"] == (
        approval.EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST
    )
    assert package["split_event_evidence_results_review_package_digest"] == (
        approval.EXPECTED_SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST
    )
    assert package["corporate_action_authority_plan_approval_digest"] == (
        approval.EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST
    )
    assert package["post_identity_freeze_registry_inventory_approval_digest"] == (
        approval.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST
    )
    assert package["identity_authority_freeze_digest"] == (
        approval.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST
    )
    assert package["target_universe"] == approval.TARGET_UNIVERSE
    assert package["target_universe_count"] == 12


def test_request_objective_scope_policy_and_planned_outputs_are_preserved():
    package = _package()

    assert package["dividend_provider_evidence_request_objective"] == (
        approval.DIVIDEND_PROVIDER_EVIDENCE_REQUEST_OBJECTIVE
    )
    assert package["dividend_provider_evidence_request_scope"] == (
        approval.DIVIDEND_PROVIDER_EVIDENCE_REQUEST_SCOPE
    )
    assert package["dividend_provider_evidence_authority_scope"] == (
        approval.DIVIDEND_PROVIDER_EVIDENCE_AUTHORITY_SCOPE
    )
    assert package["dividend_provider_evidence_execution_status"] == approval.NOT_EXECUTED
    assert package["read_only_request_policy"] == approval.READ_ONLY_REQUEST_POLICY
    assert package["planned_output_count"] == len(
        approval.PLANNED_DIVIDEND_EVIDENCE_OUTPUT_NAMES
    )
    assert all(
        item["generation_status"] == approval.PLANNED_NOT_GENERATED
        and item["generated"] is False
        and item["actionability"] == approval.RESEARCH_ONLY_NON_ACTIONABLE
        for item in package["planned_outputs"]
    )


def test_per_ticker_approval_entries_bind_sources_and_keep_runtime_closed():
    package = _package()
    entries = package["per_ticker_dividend_provider_evidence_request_approvals"]

    assert len(entries) == 12
    assert [entry["ticker"] for entry in entries] == approval.TARGET_UNIVERSE
    for entry in entries:
        assert entry["dividend_event_candidate_status"] == (
            approval.dividend_review.candidate_service.DIVIDEND_EVENT_CANDIDATE_READY_FOR_OPERATOR_REVIEW
        )
        assert entry["dividend_event_review_status"] == (
            approval.dividend_review.READY_FOR_OPERATOR_ASSESSMENT
        )
        assert entry["dividend_provider_evidence_request_status"] == (
            approval.AUTHORIZED_NOT_EXECUTED
        )
        assert entry["dividend_provider_evidence_execution_status"] == approval.NOT_EXECUTED
        assert entry["dividend_provider_evidence_results_status"] == approval.NOT_CREATED
        assert entry["dividend_event_authority_status"] == approval.NOT_CREATED
        assert entry["dividend_event_freeze_status"] == approval.NOT_FROZEN
        assert entry["split_event_authority_status"] == "FROZEN"
        assert entry["corporate_action_authority_created"] is False
        assert entry["acquisition_authorized"] is False
        assert entry["dataset_generation_authorized"] is False
        assert entry["runtime_use"] == approval.NOT_AUTHORIZED
        assert entry["strategy_use"] == approval.NOT_AUTHORIZED
        assert entry["paper_trading"] == approval.NOT_AUTHORIZED
        assert entry["broker_execution"] == approval.NOT_AUTHORIZED
        assert len(entry["source_dividend_event_candidate_digest"]) == 64
        assert len(entry["source_dividend_event_review_digest"]) == 64
        assert entry["source_split_event_authority_freeze_digest"] == (
            approval.EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST
        )
        assert entry["source_corporate_action_plan_approval_digest"] == (
            approval.EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST
        )
        assert len(
            entry["per_ticker_dividend_provider_evidence_request_approval_digest"]
        ) == 64


def test_checklist_summary_and_remaining_roadmap():
    package = _package()

    assert [item["check_id"] for item in package["approval_checklist"]] == (
        approval.REQUIRED_APPROVAL_CHECK_IDS
    )
    assert all(item["status"] == approval.PASS for item in package["approval_checklist"])
    assert package["approval_summary"]["total_checks"] == len(
        approval.REQUIRED_APPROVAL_CHECK_IDS
    )
    assert package["approval_summary"]["failed_checks"] == 0
    assert package["approval_summary"]["blocker_count"] == 0
    assert package["approval_summary"][
        "dividend_provider_evidence_request_authorized_by_operator"
    ] is True
    assert package["remaining_required_tasks"] == approval.REMAINING_REQUIRED_TASKS


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("provider_requests_made_in_approval", False),
        ("live_provider_transport_enabled_in_approval", False),
        ("dividend_provider_evidence_executed", False),
        ("dividend_provider_evidence_results_created", False),
        ("dividend_event_authority_created", False),
        ("dividend_event_authority_frozen", False),
        ("split_event_authority_created", True),
        ("split_event_authority_frozen", True),
        ("split_provider_evidence_rerun_performed", False),
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
        ("feature_matrix_regeneration_performed", False),
        ("new_strategy_scoring_performed", False),
        ("trade_recommendations_generated", False),
        ("predictive_usefulness", approval.NOT_ACCEPTED),
        ("profitability", approval.PROFITABILITY_NOT_ACCEPTED),
        ("runtime_migration_approved", False),
        ("runtime_use", approval.NOT_AUTHORIZED),
        ("strategy_use", approval.NOT_AUTHORIZED),
        ("paper_trading", approval.NOT_AUTHORIZED),
        ("broker_execution", approval.NOT_AUTHORIZED),
        ("automatic_stitching", False),
    ],
)
def test_authority_execution_predictive_and_runtime_boundaries(field: str, expected: Any):
    package = _package()

    assert package[field] == expected


@pytest.mark.parametrize(
    "override",
    [
        {"operator_decision": "APPROVE_SOMETHING_ELSE"},
        {"operator_attestation_phrase": "wrong"},
        {"operator_confirms_dividend_candidate_review_package_digest": "0" * 64},
        {"operator_confirms_dividend_candidate_digest": "0" * 64},
        {"operator_confirms_split_event_authority_freeze_digest": "0" * 64},
        {"operator_confirms_split_evidence_results_review_package_digest": "0" * 64},
        {"operator_confirms_corporate_action_plan_approval_digest": "0" * 64},
        {"operator_confirms_registry_inventory_approval_digest": "0" * 64},
        {"operator_confirms_identity_freeze_digest": "0" * 64},
        {"operator_confirms_target_universe": list(reversed(approval.TARGET_UNIVERSE))},
        {"operator_confirms_target_count": 11},
        {"operator_confirms_request_scope_read_only_dividend_event_evidence_only": False},
        {"operator_confirms_ready_for_dividend_provider_evidence_execution": False},
        {"operator_confirms_no_provider_requests_made_in_approval": False},
        {"operator_confirms_no_live_provider_transport_enabled": False},
        {"operator_confirms_no_dividend_provider_evidence_executed": False},
        {"operator_confirms_no_dividend_provider_evidence_results_created": False},
        {"operator_confirms_no_dividend_event_authority_created": False},
        {"operator_confirms_no_dividend_event_authority_frozen": False},
        {"operator_confirms_split_event_authority_frozen": False},
        {"operator_confirms_no_split_provider_evidence_rerun": False},
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
    with pytest.raises(approval.DividendProviderEvidenceRequestApprovalError):
        _package(**override)


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("artifact_kind", "WRONG"),
        ("approval_status", "WRONG"),
        ("approval_scope", "WRONG"),
        ("dividend_provider_evidence_request_authorized", False),
        ("ready_for_dividend_provider_evidence_execution", False),
        ("provider_requests_made_in_approval", True),
        ("live_provider_transport_enabled_in_approval", True),
        ("dividend_provider_evidence_executed", True),
        ("dividend_provider_evidence_results_created", True),
        ("dividend_event_authority_created", True),
        ("dividend_event_authority_frozen", True),
        ("split_event_authority_created", False),
        ("split_event_authority_frozen", False),
        ("split_provider_evidence_rerun_performed", True),
        ("corporate_action_authority_created", True),
        ("target_universe_count", 11),
        ("target_universe", list(reversed(approval.TARGET_UNIVERSE))),
        ("new_ticker_acquisition_authorized", True),
        ("dataset_generation_authorized", True),
        ("additional_predictive_evidence_execution_authorized", True),
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

    with pytest.raises(approval.DividendProviderEvidenceRequestApprovalError):
        approval.validate_dividend_provider_evidence_request_approved_v1(package)


def test_validator_rejects_missing_per_ticker_digest_and_approval_digest():
    package = _package()
    del package["per_ticker_dividend_provider_evidence_request_approvals"][0][
        "per_ticker_dividend_provider_evidence_request_approval_digest"
    ]

    with pytest.raises(approval.DividendProviderEvidenceRequestApprovalError):
        approval.validate_dividend_provider_evidence_request_approved_v1(package)

    package = _package()
    del package["dividend_provider_evidence_request_approval_digest"]
    with pytest.raises(approval.DividendProviderEvidenceRequestApprovalError):
        approval.validate_dividend_provider_evidence_request_approved_v1(package)


def test_approval_and_per_ticker_digests_are_deterministic():
    first = _package()
    second = _package()

    assert first["dividend_provider_evidence_request_approval_digest"] == (
        second["dividend_provider_evidence_request_approval_digest"]
    )
    assert [
        item["per_ticker_dividend_provider_evidence_request_approval_digest"]
        for item in first["per_ticker_dividend_provider_evidence_request_approvals"]
    ] == [
        item["per_ticker_dividend_provider_evidence_request_approval_digest"]
        for item in second["per_ticker_dividend_provider_evidence_request_approvals"]
    ]


def test_markdown_includes_required_sections_and_guardrails():
    markdown = approval.build_dividend_provider_evidence_request_approved_markdown_v1(
        _package()
    )

    for heading in [
        "## Approved Dividend Provider Evidence Request",
        "## Operator Attestation",
        "## Source Dividend Candidate Review Package",
        "## Source Split Authority Freeze",
        "## Target Universe",
        "## Approval Scope",
        "## Read-Only Provider Request Boundary",
        "## Dividend Evidence Execution Boundary",
        "## Dividend Authority Boundary",
        "## Split Authority Boundary",
        "## Corporate-Action Authority Boundary",
        "## Acquisition Boundary",
        "## Dataset Boundary",
        "## Predictive/Profitability Boundary",
        "## Runtime Boundary",
        "## Approval Checklist Summary",
        "## Remaining Required Tasks",
        "## Guardrails",
    ]:
        assert heading in markdown
    assert "No dividend provider evidence execution occurred." in markdown
    assert "No dividend authority or freeze was created." in markdown


def test_writer_writes_json_and_markdown_without_overwrite(tmp_path: Path):
    result = approval.write_dividend_provider_evidence_request_approved_v1(
        tmp_path,
        dividend_candidate_review_package=_dividend_review_package(),
        split_authority_freeze_artifact=_split_freeze_artifact(),
        operator_attestation=_attestation(),
    )

    assert Path(result["json_path"]).is_file()
    assert Path(result["markdown_path"]).is_file()
    assert result["validation"]["status"] == "DIVIDEND_PROVIDER_EVIDENCE_REQUEST_APPROVED_VALID"
    with pytest.raises(approval.DividendProviderEvidenceRequestApprovalError):
        approval.write_dividend_provider_evidence_request_approved_v1(
            tmp_path,
            dividend_candidate_review_package=_dividend_review_package(),
            split_authority_freeze_artifact=_split_freeze_artifact(),
            operator_attestation=_attestation(),
        )


def test_public_exports_are_available():
    assert services.ARTIFACT_KIND_DIVIDEND_PROVIDER_EVIDENCE_REQUEST_APPROVED == (
        approval.ARTIFACT_KIND_DIVIDEND_PROVIDER_EVIDENCE_REQUEST_APPROVED
    )
    assert services.DIVIDEND_PROVIDER_EVIDENCE_REQUEST_APPROVED == (
        approval.DIVIDEND_PROVIDER_EVIDENCE_REQUEST_APPROVED
    )
    assert services.build_dividend_provider_evidence_request_approved_v1 is (
        approval.build_dividend_provider_evidence_request_approved_v1
    )
