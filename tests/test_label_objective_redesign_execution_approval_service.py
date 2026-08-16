from __future__ import annotations

import json
from copy import deepcopy
from unittest.mock import patch

import pytest

from marketflow.services import (
    label_objective_redesign_execution_approval_service as approval,
)


def _attestation(**overrides) -> dict:
    kwargs = {
        "operator_reference": "TEST_OPERATOR",
        "operator_attestation_timestamp_utc": "2026-08-16T12:00:00Z",
        "operator_attestation_phrase": (
            approval.REQUIRED_LABEL_OBJECTIVE_REDESIGN_EXECUTION_APPROVAL_ATTESTATION_PHRASE
        ),
        "operator_confirms_target_universe": list(approval.TARGET_UNIVERSE),
        "operator_confirms_target_count": 12,
        "operator_confirms_meta_record_count": 913,
        "operator_confirms_non_meta_record_count": 1003,
        "operator_confirms_selected_method_path": approval.SELECTED_METHOD_PATH,
        **approval._expected_digest_confirmations(),
        **{
            field: True
            for field in approval.REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS
        },
    }
    kwargs.update(overrides)
    return approval.build_label_objective_redesign_execution_approval_attestation_v1(
        **kwargs
    )


@pytest.fixture(scope="module")
def source_review() -> dict:
    return approval.review_service.build_label_objective_redesign_execution_candidate_review_package_v1()


def _build(source_review: dict, attestation: dict | None = None) -> dict:
    return approval.build_label_objective_redesign_execution_approved_v1(
        execution_candidate_review_package=deepcopy(source_review),
        operator_attestation=_attestation() if attestation is None else attestation,
    )


def _validate(artifact: dict, source_review: dict) -> dict:
    with patch.object(
        approval, "_source_review", return_value=deepcopy(source_review)
    ):
        return approval.validate_label_objective_redesign_execution_approved_v1(
            artifact
        )


@pytest.fixture(scope="module")
def approved(source_review: dict) -> dict:
    return _build(source_review)


def test_attestation_builder_creates_all_required_fields() -> None:
    attestation = _attestation()
    assert attestation["operator_decision"] == (
        "APPROVE_LABEL_OBJECTIVE_REDESIGN_EXECUTION"
    )
    assert attestation["operator_attestation_phrase"] == (
        "APPROVE LABEL OBJECTIVE REDESIGN EXECUTION MSFT NVDA AMZN GOOGL "
        "META TSLA JPM XOM JNJ WMT CAT LMT "
        "LABEL_OBJECTIVE_REDESIGN_EXECUTION_APPROVAL_ONLY"
    )
    assert attestation["operator_attestation_version"] == (
        "label_objective_redesign_execution_approval_operator_attestation_v1"
    )
    assert attestation["operator_reference"] == "TEST_OPERATOR"
    assert all(
        attestation[field] is True
        for field in approval.REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS
    )


def test_approval_builds_offline(
    source_review: dict, monkeypatch: pytest.MonkeyPatch
) -> None:
    def forbidden_connect(*_args, **_kwargs):
        raise AssertionError("network access is forbidden")

    monkeypatch.setattr("socket.socket.connect", forbidden_connect)
    artifact = _build(source_review)
    assert artifact["created_offline"] is True
    assert artifact["provider_requests_made"] is False
    assert artifact["market_data_acquisition_performed"] is False


def test_default_source_review_builder_path_is_supported(
    source_review: dict,
) -> None:
    validation = {
        "label_objective_redesign_execution_candidate_review_package_digest": (
            approval.EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST
        )
    }
    with (
        patch.object(
            approval.review_service,
            "build_label_objective_redesign_execution_candidate_review_package_v1",
            return_value=deepcopy(source_review),
        ),
        patch.object(
            approval.review_service,
            "validate_label_objective_redesign_execution_candidate_review_package_v1",
            return_value=validation,
        ),
    ):
        artifact = approval.build_label_objective_redesign_execution_approved_v1(
            operator_attestation=_attestation()
        )
    assert artifact["label_objective_redesign_execution_approved"] is True


def test_artifact_schema_status_and_scope_are_exact(approved: dict) -> None:
    assert approved["artifact_kind"] == (
        "LABEL_OBJECTIVE_REDESIGN_EXECUTION_APPROVED"
    )
    assert approved["schema_version"] == (
        "label_objective_redesign_execution_approval_v1"
    )
    assert approved["approval_status"] == (
        "LABEL_OBJECTIVE_REDESIGN_EXECUTION_APPROVED"
    )
    assert approved["approval_scope"] == (
        "LABEL_OBJECTIVE_REDESIGN_EXECUTION_APPROVAL_ONLY"
    )


@pytest.mark.parametrize(
    ("field", "expected"), list(approval.REQUIRED_DIGEST_FIELDS.items())
)
def test_all_required_source_digests_are_bound(
    approved: dict, field: str, expected: str
) -> None:
    assert approved[field] == expected


def test_dataset_universe_and_counts_are_preserved(approved: dict) -> None:
    assert approved["dataset_name"] == "expanded_universe_canonical_dataset_v1"
    assert approved["source_profile"] == "RTH_FULL_SESSION_1D"
    assert approved["timeframe"] == "1d"
    assert approved["date_range_start"] == "2022-01-01"
    assert approved["date_range_end"] == "2025-12-31"
    assert approved["target_universe"] == approval.TARGET_UNIVERSE
    assert approved["target_universe_count"] == 12
    assert approved["total_canonical_record_count"] == 11946
    assert approved["meta_record_count"] == 913
    assert approved["non_meta_record_count"] == 1003
    assert approved["meta_reduced_record_count_preserved"] is True
    assert all(
        approved["per_ticker_record_counts"][ticker]
        == (913 if ticker == "META" else 1003)
        for ticker in approval.TARGET_UNIVERSE
    )


def test_selected_method_and_execution_objective_are_exact(approved: dict) -> None:
    assert approved["selected_method_path"] == (
        "OPTION_C_LABEL_OBJECTIVE_REDESIGN_CANDIDATE"
    )
    assert approved["label_objective_redesign_execution_objective"] == (
        "EXECUTE_LABEL_OBJECTIVE_REDESIGN_PLANNING_OUTPUTS_FOR_APPROVED_REDESIGN_PLAN"
    )
    assert approved["label_objective_redesign_execution_scope"] == (
        "LABEL_OBJECTIVE_REDESIGN_EXECUTION_APPROVAL_ONLY"
    )
    assert approved["label_objective_redesign_execution_mode"] == (
        "AUTHORIZED_NOT_EXECUTED"
    )
    assert approved["label_objective_redesign_execution_authority_status"] == (
        "AUTHORIZED_FOR_FUTURE_LABEL_OBJECTIVE_REDESIGN_EXECUTION_ONLY"
    )


def test_execution_approval_authorizes_only_future_redesign_execution(
    approved: dict,
) -> None:
    assert approved["label_objective_redesign_execution_approval_created"] is True
    assert approved["label_objective_redesign_execution_approved"] is True
    assert approved["label_objective_redesign_authorized"] is True
    assert approved["ready_for_label_objective_redesign_execution"] is True


@pytest.mark.parametrize(
    "field",
    [
        "label_objective_redesign_executed",
        "label_objective_redesign_results_created",
        "redesigned_label_generation_authorized",
        "redesigned_label_generation_performed",
        "redesigned_feature_generation_authorized",
        "redesigned_feature_generation_performed",
        "redesigned_protocol_evaluation_authorized",
        "redesigned_protocol_evaluation_performed",
        "additional_predictive_evidence_execution_candidate_created",
        "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
    ],
)
def test_execution_results_generation_and_downstream_actions_remain_false(
    approved: dict, field: str
) -> None:
    assert approved[field] is False


def test_predictive_profitability_runtime_and_trading_remain_closed(
    approved: dict,
) -> None:
    assert approved["predictive_usefulness"] == "not accepted"
    assert approved["predictive_usefulness_acceptance_candidate_created"] is False
    assert approved["profitability"] == "not accepted"
    assert approved["runtime_migration_approved"] is False
    assert approved["runtime_migration_active"] is False
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        assert approved[field] == "NOT_AUTHORIZED"


def test_approved_execution_activities_are_exact_and_unexecuted(
    approved: dict,
) -> None:
    rows = approved["approved_execution_activities"]
    expected = approval.review_service.candidate_service.PLANNED_EXECUTION_ACTIVITIES
    assert len(rows) == 14
    assert [row["activity_id"] for row in rows] == expected
    assert all(row["authorization_status"] == "AUTHORIZED_NOT_EXECUTED" for row in rows)
    assert all(row["execution_status"] == "NOT_EXECUTED" for row in rows)
    assert all(row["research_only"] is True and row["non_actionable"] is True for row in rows)


def test_approved_workstreams_are_exact_and_unexecuted(approved: dict) -> None:
    rows = approved["approved_workstreams"]
    expected = approval.review_service.candidate_service.PLANNED_WORKSTREAMS
    assert len(rows) == 10
    assert [row["workstream_id"] for row in rows] == expected
    assert all(row["authorization_status"] == "AUTHORIZED_NOT_EXECUTED" for row in rows)
    assert all(row["execution_status"] == "NOT_EXECUTED" for row in rows)


def test_future_label_family_outputs_are_authorized_not_generated(
    approved: dict,
) -> None:
    rows = approved["future_label_family_outputs"]
    assert len(rows) == 10
    assert [row["label_family_candidate_id"] for row in rows] == (
        approval.review_service.candidate_service.candidate_service.LABEL_FAMILY_CANDIDATES
    )
    assert all(row["planned_output_status"] == "AUTHORIZED_NOT_GENERATED" for row in rows)
    assert all(row["label_generation_authorized"] is False for row in rows)
    assert all(row["label_generation_performed"] is False for row in rows)


def test_future_execution_outputs_are_authorized_not_generated(
    approved: dict,
) -> None:
    rows = approved["future_execution_outputs"]
    assert len(rows) == 8
    assert [row["output_id"] for row in rows] == (
        approval.review_service.candidate_service.PLANNED_EXECUTION_OUTPUTS
    )
    assert all(row["output_status"] == "AUTHORIZED_NOT_GENERATED" for row in rows)
    assert all(row["authority"] == "RESEARCH_ONLY_NON_ACTIONABLE" for row in rows)


def test_per_ticker_approval_entries_preserve_order_counts_and_boundaries(
    approved: dict,
) -> None:
    entries = approved["per_ticker_approval_entries"]
    assert len(entries) == 12
    assert [entry["ticker"] for entry in entries] == approval.TARGET_UNIVERSE
    for entry in entries:
        ticker = entry["ticker"]
        assert entry["historical_record_count"] == (913 if ticker == "META" else 1003)
        assert entry["selected_method_path"] == approval.SELECTED_METHOD_PATH
        assert entry["label_objective_redesign_execution_candidate_status"] == (
            "REVIEWED_READY_FOR_OPERATOR_ASSESSMENT"
        )
        assert entry["label_objective_redesign_execution_approval_status"] == (
            approval.AUTHORIZED_FOR_FUTURE_LABEL_OBJECTIVE_REDESIGN_EXECUTION_ONLY
        )
        assert entry["label_objective_redesign_authorized"] is True
        assert entry["label_objective_redesign_executed"] is False
        assert entry["redesigned_label_generation_authorized"] is False
        assert entry["redesigned_label_generation_performed"] is False
        assert entry["runtime_use"] == "NOT_AUTHORIZED"


def test_meta_per_ticker_entry_preserves_limitation(approved: dict) -> None:
    entries = {entry["ticker"]: entry for entry in approved["per_ticker_approval_entries"]}
    assert entries["META"]["historical_record_count"] == 913
    assert entries["META"]["meta_reduced_record_count_flag"] is True
    assert entries["META"]["redesign_note"] == (
        "PRESERVE_REDUCED_RECORD_COUNT_AND_LABEL_AVAILABILITY_LIMITATION"
    )
    assert all(
        entry["historical_record_count"] == 1003
        and entry["meta_reduced_record_count_flag"] is False
        for ticker, entry in entries.items()
        if ticker != "META"
    )


def test_per_ticker_approval_digests_are_present_and_deterministic(
    approved: dict,
) -> None:
    for entry in approved["per_ticker_approval_entries"]:
        digest = entry[
            "per_ticker_label_objective_redesign_execution_approval_digest"
        ]
        assert len(digest) == 64
        assert digest == (
            approval.per_ticker_label_objective_redesign_execution_approval_digest_v1(
                entry
            )
        )
        assert entry[
            "source_label_objective_redesign_execution_candidate_review_digest"
        ] == approval.EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST
        assert entry[
            "source_label_objective_redesign_execution_candidate_digest"
        ] == approval.EXPECTED_EXECUTION_CANDIDATE_DIGEST


def test_next_chain_gates_and_risk_controls_are_exact(approved: dict) -> None:
    assert approved["next_chain"] == approval.NEXT_CHAIN
    assert len(approved["next_chain"]) == 8
    assert approved["next_gates"] == approval.NEXT_GATES
    assert len(approved["next_gates"]) == 10
    assert approved["risk_controls"] == approval.RISK_CONTROLS
    assert len(approved["risk_controls"]) == 14


def test_approval_checklist_and_summary_pass(approved: dict) -> None:
    assert len(approved["approval_checklist"]) == len(approval.CHECK_IDS) == 60
    assert all(item["status"] == "PASS" for item in approved["approval_checklist"])
    assert all(
        set(item)
        == {"check_id", "status", "expected", "actual", "severity", "message"}
        for item in approved["approval_checklist"]
    )
    assert approved["approval_summary"] == {
        "total_checks": 60,
        "passed_checks": 60,
        "failed_checks": 0,
        "blocker_count": 0,
        "label_objective_redesign_execution_approved_by_operator": True,
        "approval_scope": "LABEL_OBJECTIVE_REDESIGN_EXECUTION_APPROVAL_ONLY",
        "label_objective_redesign_authorized": True,
        "ready_for_label_objective_redesign_execution": True,
        "label_objective_redesign_executed": False,
        "label_objective_redesign_results_created": False,
        "redesigned_label_generation_authorized": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def test_approval_digest_is_deterministic(
    approved: dict, source_review: dict
) -> None:
    second = _build(source_review)
    assert second == approved
    assert approved["label_objective_redesign_execution_approval_digest"] == (
        approval.label_objective_redesign_execution_approval_digest_v1(approved)
    )
    assert [
        entry["per_ticker_label_objective_redesign_execution_approval_digest"]
        for entry in second["per_ticker_approval_entries"]
    ] == [
        entry["per_ticker_label_objective_redesign_execution_approval_digest"]
        for entry in approved["per_ticker_approval_entries"]
    ]


def test_validator_accepts_valid_approval(
    approved: dict, source_review: dict
) -> None:
    result = _validate(approved, source_review)
    assert result["status"] == "LABEL_OBJECTIVE_REDESIGN_EXECUTION_APPROVAL_VALID"
    assert result["label_objective_redesign_execution_approved"] is True
    assert result["label_objective_redesign_authorized"] is True
    assert result["ready_for_label_objective_redesign_execution"] is True
    assert result["label_objective_redesign_executed"] is False
    assert result["blocker_count"] == 0


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("artifact_kind", "WRONG"),
        ("approval_status", "WRONG"),
        ("approval_scope", "WRONG"),
        ("label_objective_redesign_execution_candidate_review_package_digest", "0" * 64),
        ("label_objective_redesign_execution_candidate_digest", "0" * 64),
        ("label_objective_redesign_approval_digest", "0" * 64),
        ("records_digest", "0" * 64),
        ("target_universe", list(reversed(approval.TARGET_UNIVERSE))),
        ("target_universe_count", 11),
        ("meta_record_count", 1003),
        ("selected_method_path", "WRONG"),
        ("label_objective_redesign_execution_approved", False),
        ("label_objective_redesign_authorized", False),
        ("ready_for_label_objective_redesign_execution", False),
        ("label_objective_redesign_executed", True),
        ("label_objective_redesign_results_created", True),
        ("redesigned_label_generation_authorized", True),
        ("redesigned_label_generation_performed", True),
        ("additional_predictive_evidence_execution_candidate_created", True),
        ("predictive_usefulness", "accepted"),
        ("profitability", "accepted"),
        ("runtime_use", "AUTHORIZED"),
        ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
        ("trade_recommendations_generated", True),
    ],
)
def test_validator_rejects_changed_or_forbidden_top_level_values(
    approved: dict, source_review: dict, field: str, bad_value: object
) -> None:
    mutated = deepcopy(approved)
    mutated[field] = bad_value
    with pytest.raises(approval.LabelObjectiveRedesignExecutionApprovalError):
        _validate(mutated, source_review)


@pytest.mark.parametrize(
    "field",
    [
        "label_objective_redesign_execution_candidate_review_package_digest",
        "label_objective_redesign_execution_candidate_digest",
        "label_objective_redesign_approval_digest",
        "records_digest",
        "risk_controls",
        "label_objective_redesign_execution_approval_digest",
    ],
)
def test_validator_rejects_missing_required_evidence(
    approved: dict, source_review: dict, field: str
) -> None:
    mutated = deepcopy(approved)
    mutated.pop(field)
    with pytest.raises(approval.LabelObjectiveRedesignExecutionApprovalError):
        _validate(mutated, source_review)


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("operator_decision", "WRONG"),
        ("operator_attestation_phrase", "WRONG"),
        ("operator_confirms_selected_method_path", "WRONG"),
    ],
)
def test_validator_rejects_wrong_operator_attestation_values(
    approved: dict,
    source_review: dict,
    field: str,
    bad_value: object,
) -> None:
    mutated = deepcopy(approved)
    mutated["operator_attestation"][field] = bad_value
    with pytest.raises(approval.LabelObjectiveRedesignExecutionApprovalError):
        _validate(mutated, source_review)


@pytest.mark.parametrize(
    "field", approval.REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS
)
def test_builder_rejects_missing_operator_boundary_confirmation(
    source_review: dict, field: str
) -> None:
    with pytest.raises(approval.LabelObjectiveRedesignExecutionApprovalError):
        _build(source_review, _attestation(**{field: False}))


@pytest.mark.parametrize(
    "field", list(approval._expected_digest_confirmations())
)
def test_builder_rejects_wrong_operator_digest_confirmation(
    source_review: dict, field: str
) -> None:
    with pytest.raises(approval.LabelObjectiveRedesignExecutionApprovalError):
        _build(source_review, _attestation(**{field: "0" * 64}))


def test_validator_rejects_missing_per_ticker_approval_digest(
    approved: dict, source_review: dict
) -> None:
    mutated = deepcopy(approved)
    mutated["per_ticker_approval_entries"][0].pop(
        "per_ticker_label_objective_redesign_execution_approval_digest"
    )
    with pytest.raises(approval.LabelObjectiveRedesignExecutionApprovalError):
        _validate(mutated, source_review)


def test_markdown_includes_all_required_sections(approved: dict) -> None:
    markdown = approval.build_label_objective_redesign_execution_approved_markdown_v1(
        approved
    )
    headings = [
        "Title",
        "Label Objective Redesign Execution Approval",
        "Operator Attestation",
        "Bound Evidence",
        "Dataset and Universe",
        "Approved Execution Objective",
        "Approved Execution Activities",
        "Approved Workstreams",
        "Future Label Family Outputs",
        "Future Execution Outputs",
        "Per-Ticker Approval Entries",
        "Next Chain",
        "Next Gates",
        "Risk Controls",
        "Checklist Summary",
        "Guardrails",
    ]
    assert all(f"## {heading}" in markdown for heading in headings)
    assert "does not execute redesign" in markdown


def test_writer_uses_canonical_json_and_refuses_overwrite(
    tmp_path, approved: dict, source_review: dict
) -> None:
    result = approval.write_label_objective_redesign_execution_approved_v1(
        tmp_path,
        execution_candidate_review_package=deepcopy(source_review),
        operator_attestation=_attestation(),
    )
    path = tmp_path / result["filename"]
    assert json.loads(path.read_text(encoding="utf-8")) == approved
    assert result["payload_sha256"]
    with pytest.raises(approval.LabelObjectiveRedesignExecutionApprovalError):
        approval.write_label_objective_redesign_execution_approved_v1(
            tmp_path,
            execution_candidate_review_package=deepcopy(source_review),
            operator_attestation=_attestation(),
        )
