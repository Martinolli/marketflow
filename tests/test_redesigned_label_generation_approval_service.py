from __future__ import annotations

import json
from copy import deepcopy
from unittest.mock import patch

import pytest

from marketflow.services import redesigned_label_generation_approval_service as approval


def _attestation(**overrides) -> dict:
    kwargs = {
        "operator_reference": "TEST_OPERATOR",
        "operator_attestation_timestamp_utc": "2026-08-17T12:00:00Z",
        "operator_attestation_phrase": (
            approval.REQUIRED_REDESIGNED_LABEL_GENERATION_APPROVAL_ATTESTATION_PHRASE
        ),
        "operator_confirms_target_universe": list(approval.TARGET_UNIVERSE),
        "operator_confirms_target_count": 12,
        "operator_confirms_meta_record_count": 913,
        "operator_confirms_non_meta_record_count": 1003,
        **approval._expected_attestation_digests(),
        **{
            field: True
            for field in approval.REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS
        },
    }
    kwargs.update(overrides)
    return approval.build_redesigned_label_generation_approval_attestation_v1(
        **kwargs
    )


@pytest.fixture(scope="module")
def source_review() -> dict:
    return approval.review_service.build_redesigned_label_generation_candidate_review_package_v1()


def _build(source_review: dict, attestation: dict | None = None) -> dict:
    return approval.build_redesigned_label_generation_approved_v1(
        candidate_review_package=deepcopy(source_review),
        operator_attestation=_attestation() if attestation is None else attestation,
    )


def _validate(artifact: dict, source_review: dict) -> dict:
    with patch.object(
        approval, "_source_review", return_value=deepcopy(source_review)
    ):
        return approval.validate_redesigned_label_generation_approved_v1(artifact)


@pytest.fixture(scope="module")
def approved(source_review: dict) -> dict:
    return _build(source_review)


def test_attestation_builder_creates_required_fields() -> None:
    attestation = _attestation()
    assert attestation["operator_decision"] == (
        "APPROVE_REDESIGNED_LABEL_GENERATION"
    )
    assert attestation["operator_attestation_phrase"] == (
        "APPROVE REDESIGNED LABEL GENERATION MSFT NVDA AMZN GOOGL META TSLA "
        "JPM XOM JNJ WMT CAT LMT REDESIGNED_LABEL_GENERATION_APPROVAL_ONLY"
    )
    assert attestation["operator_attestation_version"] == (
        "redesigned_label_generation_approval_operator_attestation_v1"
    )
    assert attestation["operator_reference"] == "TEST_OPERATOR"
    assert all(
        attestation[field] is True
        for field in approval.REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS
    )


def test_approval_package_builds_offline(
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
        "redesigned_label_generation_candidate_review_package_digest": (
            approval.EXPECTED_CANDIDATE_REVIEW_PACKAGE_DIGEST
        )
    }
    with (
        patch.object(
            approval.review_service,
            "build_redesigned_label_generation_candidate_review_package_v1",
            return_value=deepcopy(source_review),
        ),
        patch.object(
            approval.review_service,
            "validate_redesigned_label_generation_candidate_review_package_v1",
            return_value=validation,
        ),
    ):
        artifact = approval.build_redesigned_label_generation_approved_v1(
            operator_attestation=_attestation()
        )
    assert artifact["redesigned_label_generation_approved"] is True


def test_artifact_kind_status_scope_and_schema_are_exact(approved: dict) -> None:
    assert approved["artifact_kind"] == "REDESIGNED_LABEL_GENERATION_APPROVED"
    assert approved["schema_version"] == (
        "redesigned_label_generation_approval_v1"
    )
    assert approved["approval_status"] == "REDESIGNED_LABEL_GENERATION_APPROVED"
    assert approved["approval_scope"] == (
        "REDESIGNED_LABEL_GENERATION_APPROVAL_ONLY"
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


def test_source_design_artifacts_are_reviewed_and_preserved(approved: dict) -> None:
    assert approved["source_label_objective_redesign_output_root"] == (
        ".marketflow/label_objective_redesign/expanded_universe_v1/"
    )
    assert approved["source_label_objective_redesign_output_count"] == 8
    assert approved["source_label_objective_redesign_output_status"] == (
        "REVIEWED_AND_VERIFIED"
    )
    assert approved["label_family_candidate_count"] == 10
    assert approved["threshold_design_strategy_count"] == 7
    assert approved["horizon_design_candidate_count"] == 5
    assert approved["per_ticker_plan_count"] == 12


def test_approval_objective_mode_and_authority_are_exact(approved: dict) -> None:
    assert approved["redesigned_label_generation_objective"] == (
        "GENERATE_REDESIGNED_LABELS_FROM_REVIEWED_LABEL_OBJECTIVE_DESIGN_ARTIFACTS"
    )
    assert approved["redesigned_label_generation_scope"] == (
        "REDESIGNED_LABEL_GENERATION_APPROVAL_ONLY"
    )
    assert approved["redesigned_label_generation_mode"] == (
        "AUTHORIZED_NOT_GENERATED"
    )
    assert approved["redesigned_label_generation_authority_status"] == (
        "AUTHORIZED_FOR_FUTURE_REDESIGNED_LABEL_GENERATION_ONLY"
    )


def test_approval_authorization_and_ready_flags_are_true(approved: dict) -> None:
    assert approved["redesigned_label_generation_approved"] is True
    assert approved["redesigned_label_generation_authorized"] is True
    assert approved["ready_for_redesigned_label_generation_execution"] is True


@pytest.mark.parametrize(
    "field",
    [
        "redesigned_label_generation_performed",
        "actual_redesigned_labels_generated",
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
def test_generation_and_downstream_actions_remain_false(
    approved: dict, field: str
) -> None:
    assert approved[field] is False


def test_predictive_profitability_runtime_and_trading_remain_closed(
    approved: dict,
) -> None:
    assert approved["predictive_usefulness"] == "not accepted"
    assert approved["predictive_usefulness_acceptance_ready"] is False
    assert approved["predictive_usefulness_acceptance_recommended"] is False
    assert approved["profitability"] == "not accepted"
    assert approved["profitability_acceptance_ready"] is False
    assert approved["profitability_acceptance_recommended"] is False
    assert approved["runtime_migration_approved"] is False
    assert approved["runtime_migration_active"] is False
    assert approved["runtime_use"] == "NOT_AUTHORIZED"
    assert approved["strategy_use"] == "NOT_AUTHORIZED"
    assert approved["paper_trading"] == "NOT_AUTHORIZED"
    assert approved["broker_execution"] == "NOT_AUTHORIZED"


def test_approved_label_generation_inputs_count_and_states(approved: dict) -> None:
    rows = approved["approved_label_generation_inputs"]
    assert len(rows) == 8
    assert [row["source_input_id"] for row in rows] == [
        "label_objective_redesign_execution_manifest",
        "label_family_candidate_matrix",
        "threshold_design_matrix",
        "horizon_design_matrix",
        "per_ticker_label_objective_plan",
        "label_availability_boundary_plan",
        "meta_limitation_preservation_plan",
        "operator_review_summary_template",
    ]
    assert all(
        row["approval_status"] == "APPROVED_FOR_FUTURE_LABEL_GENERATION_ONLY"
        and row["generation_status"] == "NOT_GENERATED"
        and row["research_only"] is True
        and row["non_actionable"] is True
        for row in rows
    )


def test_approved_label_families_count_and_states(approved: dict) -> None:
    rows = approved["approved_redesigned_label_families"]
    assert len(rows) == 10
    assert all(
        row["label_generation_authorized"] is True
        and row["label_generation_performed"] is False
        and row["actual_label_values_created"] is False
        for row in rows
    )


def test_approved_threshold_strategies_count_and_states(approved: dict) -> None:
    rows = approved["approved_threshold_strategies"]
    assert len(rows) == 7
    assert all(
        row["threshold_computation_authorized"] is True
        and row["threshold_computation_performed"] is False
        for row in rows
    )


def test_approved_horizon_strategies_count_and_states(approved: dict) -> None:
    rows = approved["approved_horizon_strategies"]
    assert len(rows) == 5
    assert all(
        row["horizon_selection_authorized"] is True
        and row["horizon_selection_performed"] is False
        for row in rows
    )


def test_approved_availability_rules_count_and_states(approved: dict) -> None:
    rows = approved["approved_availability_rules"]
    assert len(rows) == 8
    assert all(
        row["approval_status"]
        == "APPROVED_FOR_FUTURE_LABEL_AVAILABILITY_HANDLING_ONLY"
        and row["execution_status"] == "NOT_EXECUTED"
        for row in rows
    )


def test_per_ticker_entries_preserve_order_counts_and_closed_gates(
    approved: dict,
) -> None:
    entries = approved["per_ticker_approval_entries"]
    assert len(entries) == 12
    assert [row["ticker"] for row in entries] == approval.TARGET_UNIVERSE
    for row in entries:
        assert row["historical_record_count"] == (
            913 if row["ticker"] == "META" else 1003
        )
        assert row["meta_reduced_record_count_flag"] is (row["ticker"] == "META")
        assert row["redesigned_label_generation_authorized"] is True
        assert row["redesigned_label_generation_performed"] is False
        assert row["actual_redesigned_labels_generated"] is False
        assert row["predictive_usefulness"] == "not accepted"
        assert row["profitability"] == "not accepted"
        assert row["runtime_use"] == "NOT_AUTHORIZED"
        assert row["strategy_use"] == "NOT_AUTHORIZED"
        assert row["paper_trading"] == "NOT_AUTHORIZED"
        assert row["broker_execution"] == "NOT_AUTHORIZED"


def test_meta_entry_preserves_reduced_record_note(approved: dict) -> None:
    meta = next(
        row for row in approved["per_ticker_approval_entries"] if row["ticker"] == "META"
    )
    assert meta["label_availability_note"] == (
        "PRESERVE_REDUCED_RECORD_COUNT_NO_BACKFILL_OR_SYNTHETIC_LABELS"
    )


def test_per_ticker_approval_digests_are_present_and_valid(approved: dict) -> None:
    for row in approved["per_ticker_approval_entries"]:
        digest = row["per_ticker_redesigned_label_generation_approval_digest"]
        assert len(digest) == 64
        assert digest == (
            approval.per_ticker_redesigned_label_generation_approval_digest_v1(row)
        )


def test_next_chain_and_gates_are_defined(approved: dict) -> None:
    assert approved["next_chain"] == approval.NEXT_CHAIN
    assert approved["next_gates"] == approval.NEXT_GATES
    assert len(approved["next_chain"]) == 9
    assert len(approved["next_gates"]) == 11


def test_risk_controls_are_exact(approved: dict) -> None:
    assert approved["risk_controls"] == approval.RISK_CONTROLS
    assert len(approved["risk_controls"]) == 15


def test_checklist_passes(approved: dict) -> None:
    checklist = approved["approval_checklist"]
    assert [row["check_id"] for row in checklist] == approval.CHECK_IDS
    assert all(row["status"] == "PASS" for row in checklist)
    assert all(row["severity"] == "BLOCKER" for row in checklist)
    assert all(
        set(row) == {"check_id", "status", "expected", "actual", "severity", "message"}
        for row in checklist
    )
    summary = approved["approval_summary"]
    assert summary["total_checks"] == len(approval.CHECK_IDS)
    assert summary["passed_checks"] == len(approval.CHECK_IDS)
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["redesigned_label_generation_approved_by_operator"] is True


def test_approval_digest_is_deterministic(source_review: dict) -> None:
    first = _build(source_review)
    second = _build(source_review)
    assert first["redesigned_label_generation_approval_digest"] == second[
        "redesigned_label_generation_approval_digest"
    ]


def test_per_ticker_approval_digests_are_deterministic(
    source_review: dict,
) -> None:
    first = _build(source_review)
    second = _build(source_review)
    assert [
        row["per_ticker_redesigned_label_generation_approval_digest"]
        for row in first["per_ticker_approval_entries"]
    ] == [
        row["per_ticker_redesigned_label_generation_approval_digest"]
        for row in second["per_ticker_approval_entries"]
    ]


def test_validator_accepts_valid_approval(approved: dict, source_review: dict) -> None:
    result = _validate(deepcopy(approved), source_review)
    assert result["status"] == "REDESIGNED_LABEL_GENERATION_APPROVAL_VALID"
    assert result["redesigned_label_generation_approved"] is True
    assert result["redesigned_label_generation_authorized"] is True
    assert result["redesigned_label_generation_performed"] is False


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "WRONG"),
        ("approval_status", "WRONG"),
        ("approval_scope", "WRONG"),
        ("redesigned_label_generation_approved", False),
        ("redesigned_label_generation_authorized", False),
        ("ready_for_redesigned_label_generation_execution", False),
        ("redesigned_label_generation_performed", True),
        ("actual_redesigned_labels_generated", True),
        ("redesigned_feature_generation_authorized", True),
        ("redesigned_feature_generation_performed", True),
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
def test_validator_rejects_wrong_or_forbidden_top_level_state(
    approved: dict, source_review: dict, field: str, value: object
) -> None:
    mutated = deepcopy(approved)
    mutated[field] = value
    with pytest.raises(approval.RedesignedLabelGenerationApprovalError):
        _validate(mutated, source_review)


@pytest.mark.parametrize("field", list(approval.REQUIRED_DIGEST_FIELDS))
def test_validator_rejects_missing_or_wrong_bound_digest(
    approved: dict, source_review: dict, field: str
) -> None:
    mutated = deepcopy(approved)
    mutated[field] = None
    with pytest.raises(approval.RedesignedLabelGenerationApprovalError):
        _validate(mutated, source_review)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("operator_decision", "REJECT"),
        ("operator_attestation_phrase", "WRONG"),
        ("operator_reference", ""),
        ("operator_attestation_timestamp_utc", ""),
        ("operator_confirms_target_universe", list(reversed(approval.TARGET_UNIVERSE))),
        ("operator_confirms_target_count", 11),
        ("operator_confirms_meta_record_count", 1003),
        ("operator_confirms_non_meta_record_count", 913),
    ],
)
def test_builder_rejects_wrong_attestation_value(
    source_review: dict, field: str, value: object
) -> None:
    with pytest.raises(approval.RedesignedLabelGenerationApprovalError):
        _build(source_review, _attestation(**{field: value}))


@pytest.mark.parametrize(
    "field", list(approval._expected_attestation_digests())
)
def test_builder_rejects_wrong_operator_confirmed_digest(
    source_review: dict, field: str
) -> None:
    with pytest.raises(approval.RedesignedLabelGenerationApprovalError):
        _build(source_review, _attestation(**{field: "0" * 64}))


@pytest.mark.parametrize(
    "field", approval.REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS
)
def test_builder_rejects_missing_required_true_confirmation(
    source_review: dict, field: str
) -> None:
    with pytest.raises(approval.RedesignedLabelGenerationApprovalError):
        _build(source_review, _attestation(**{field: False}))


def test_validator_rejects_missing_risk_controls(
    approved: dict, source_review: dict
) -> None:
    mutated = deepcopy(approved)
    mutated["risk_controls"] = []
    with pytest.raises(approval.RedesignedLabelGenerationApprovalError):
        _validate(mutated, source_review)


def test_validator_rejects_missing_approval_digest(
    approved: dict, source_review: dict
) -> None:
    mutated = deepcopy(approved)
    mutated.pop("redesigned_label_generation_approval_digest")
    with pytest.raises(approval.RedesignedLabelGenerationApprovalError):
        _validate(mutated, source_review)


def test_validator_rejects_missing_per_ticker_digest(
    approved: dict, source_review: dict
) -> None:
    mutated = deepcopy(approved)
    mutated["per_ticker_approval_entries"][0].pop(
        "per_ticker_redesigned_label_generation_approval_digest"
    )
    with pytest.raises(approval.RedesignedLabelGenerationApprovalError):
        _validate(mutated, source_review)


def test_source_review_digest_mismatch_is_rejected(source_review: dict) -> None:
    mutated = deepcopy(source_review)
    mutated["redesigned_label_generation_candidate_review_package_digest"] = "0" * 64
    with pytest.raises(approval.RedesignedLabelGenerationApprovalError):
        _build(mutated)


def test_markdown_includes_required_sections(approved: dict) -> None:
    markdown = approval.build_redesigned_label_generation_approved_markdown_v1(
        approved
    )
    for heading in [
        "# MarketFlow Redesigned Label Generation Approval",
        "## Title",
        "## Redesigned Label Generation Approval",
        "## Operator Attestation",
        "## Bound Evidence",
        "## Dataset and Universe",
        "## Approved Source Design Artifacts",
        "## Approved Label Generation Inputs",
        "## Approved Redesigned Label Families",
        "## Approved Threshold Strategies",
        "## Approved Horizon Strategies",
        "## Approved Availability Rules",
        "## Per-Ticker Approval Entries",
        "## Next Chain",
        "## Next Gates",
        "## Risk Controls",
        "## Checklist Summary",
        "## Guardrails",
    ]:
        assert heading in markdown
    assert "TEST_OPERATOR" in markdown
    assert "future redesigned-label generation only" in markdown


def test_writer_creates_canonical_json_without_overwrite(
    tmp_path, source_review: dict
) -> None:
    result = approval.write_redesigned_label_generation_approved_v1(
        tmp_path,
        candidate_review_package=deepcopy(source_review),
        operator_attestation=_attestation(),
    )
    path = tmp_path / result["filename"]
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["artifact_kind"] == "REDESIGNED_LABEL_GENERATION_APPROVED"
    assert result["payload_byte_size"] == len(path.read_bytes())
    with pytest.raises(approval.RedesignedLabelGenerationApprovalError):
        approval.write_redesigned_label_generation_approved_v1(
            tmp_path,
            candidate_review_package=deepcopy(source_review),
            operator_attestation=_attestation(),
        )


@pytest.mark.parametrize("filename", ["../approval.json", "approval.txt"])
def test_writer_rejects_unsafe_filename(
    tmp_path, source_review: dict, filename: str
) -> None:
    with pytest.raises(approval.RedesignedLabelGenerationApprovalError):
        approval.write_redesigned_label_generation_approved_v1(
            tmp_path,
            candidate_review_package=deepcopy(source_review),
            operator_attestation=_attestation(),
            filename=filename,
        )
