from __future__ import annotations

from copy import deepcopy
import json
from unittest.mock import patch

import pytest

from marketflow import services
from marketflow.services import (
    feature_predictive_evidence_planning_approval_redesigned_labels_service as approval,
)


def _attestation(**overrides) -> dict:
    kwargs = {
        "operator_reference": "TEST_OPERATOR",
        "operator_attestation_timestamp_utc": "2026-08-17T12:00:00Z",
        "operator_attestation_phrase": approval.REQUIRED_FEATURE_PREDICTIVE_EVIDENCE_PLANNING_APPROVAL_USING_REDESIGNED_LABELS_ATTESTATION_PHRASE,
        "operator_confirms_target_universe": list(approval.TARGET_UNIVERSE),
        "operator_confirms_target_count": 12,
        "operator_confirms_meta_record_count": 913,
        "operator_confirms_non_meta_record_count": 1003,
        **approval._expected_digest_confirmations(),
        **{
            field: True
            for field in approval.REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS
        },
    }
    kwargs.update(overrides)
    return approval.build_feature_predictive_evidence_planning_approval_using_redesigned_labels_attestation_v1(
        **kwargs
    )


@pytest.fixture(scope="module")
def source_review() -> dict:
    return approval.review_service.build_feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_package_v1()


def _build(source_review: dict, attestation: dict | None = None) -> dict:
    with patch.object(
        approval, "_source_review", return_value=deepcopy(source_review)
    ):
        return approval.build_feature_predictive_evidence_planning_approved_using_redesigned_labels_v1(
            operator_attestation=_attestation() if attestation is None else attestation
        )


def _validate(artifact: dict, source_review: dict) -> dict:
    with patch.object(
        approval, "_source_review", return_value=deepcopy(source_review)
    ):
        return approval.validate_feature_predictive_evidence_planning_approved_using_redesigned_labels_v1(
            artifact
        )


@pytest.fixture(scope="module")
def approved(source_review: dict) -> dict:
    return _build(source_review)


def test_attestation_builder_creates_required_fields() -> None:
    attestation = _attestation()
    assert attestation["operator_decision"] == (
        approval.OPERATOR_DECISION_APPROVE_FEATURE_PREDICTIVE_EVIDENCE_PLANNING_USING_REDESIGNED_LABELS
    )
    assert attestation["operator_attestation_version"] == (
        approval.OPERATOR_ATTESTATION_VERSION_FEATURE_PREDICTIVE_EVIDENCE_PLANNING_APPROVAL_USING_REDESIGNED_LABELS_V1
    )
    assert attestation["operator_reference"] == "TEST_OPERATOR"
    assert attestation["operator_attestation_timestamp_utc"] == (
        "2026-08-17T12:00:00Z"
    )
    assert attestation["operator_attestation_phrase"] == (
        approval.REQUIRED_FEATURE_PREDICTIVE_EVIDENCE_PLANNING_APPROVAL_USING_REDESIGNED_LABELS_ATTESTATION_PHRASE
    )
    assert all(
        attestation[field] is True
        for field in approval.REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS
    )


def test_approval_builds_offline_without_provider_calls(
    source_review: dict, monkeypatch: pytest.MonkeyPatch
) -> None:
    def forbidden_connect(*_args, **_kwargs):
        raise AssertionError("network access is forbidden")

    monkeypatch.setattr("socket.socket.connect", forbidden_connect)
    artifact = _build(source_review)
    assert artifact["created_offline"] is True
    assert artifact["provider_requests_made"] is False
    assert artifact["market_data_acquisition_performed"] is False


def test_default_source_review_builder_path_is_supported(source_review: dict) -> None:
    validation = {
        "feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_package_digest": approval.EXPECTED_CANDIDATE_REVIEW_PACKAGE_DIGEST
    }
    with (
        patch.object(
            approval.review_service,
            "build_feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_package_v1",
            return_value=deepcopy(source_review),
        ),
        patch.object(
            approval.review_service,
            "validate_feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_package_v1",
            return_value=validation,
        ),
    ):
        artifact = approval.build_feature_predictive_evidence_planning_approved_using_redesigned_labels_v1(
            operator_attestation=_attestation()
        )
    assert artifact["feature_predictive_evidence_planning_approved"] is True


def test_artifact_kind_status_scope_and_schema_are_exact(approved: dict) -> None:
    assert approved["artifact_kind"] == (
        approval.ARTIFACT_KIND_FEATURE_PREDICTIVE_EVIDENCE_PLANNING_APPROVED_USING_REDESIGNED_LABELS
    )
    assert approved["approval_status"] == (
        approval.FEATURE_PREDICTIVE_EVIDENCE_PLANNING_APPROVED_USING_REDESIGNED_LABELS
    )
    assert approved["approval_scope"] == (
        approval.FEATURE_PREDICTIVE_EVIDENCE_PLANNING_APPROVAL_ONLY
    )
    assert approved["schema_version"] == (
        approval.SCHEMA_VERSION_FEATURE_PREDICTIVE_EVIDENCE_PLANNING_APPROVAL_USING_REDESIGNED_LABELS_V1
    )


@pytest.mark.parametrize(
    "field,expected",
    [
        ("feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_package_digest", approval.EXPECTED_CANDIDATE_REVIEW_PACKAGE_DIGEST),
        ("feature_predictive_evidence_planning_candidate_using_redesigned_labels_digest", approval.EXPECTED_CANDIDATE_DIGEST),
        ("redesigned_label_generation_results_review_package_digest", approval.EXPECTED_RESULTS_REVIEW_DIGEST),
        ("redesigned_label_generation_execution_digest", approval.EXPECTED_EXECUTION_DIGEST),
        ("redesigned_label_generation_approval_digest", approval.EXPECTED_APPROVAL_DIGEST),
        ("redesigned_label_generation_candidate_review_package_digest", approval.EXPECTED_REDESIGNED_LABEL_CANDIDATE_REVIEW_DIGEST),
        ("redesigned_label_generation_candidate_digest", approval.EXPECTED_REDESIGNED_LABEL_CANDIDATE_DIGEST),
        ("research_registry_approval_digest", approval.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST),
        ("records_digest", approval.EXPECTED_RECORDS_DIGEST),
        ("label_values_digest", approval.EXPECTED_LABEL_VALUES_DIGEST),
    ],
)
def test_all_required_digests_are_bound(
    approved: dict, field: str, expected: str
) -> None:
    assert approved[field] == expected


def test_dataset_universe_and_meta_limitation_are_preserved(approved: dict) -> None:
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


def test_redesigned_label_profile_is_preserved_and_confirmed(approved: dict) -> None:
    assert approved["redesigned_label_output_count"] == 11
    assert approved["redesigned_label_output_status"] == "REVIEWED_AND_VERIFIED"
    assert approved["label_family_count"] == 10
    assert approved["threshold_strategy_count"] == 7
    assert approved["horizon_strategy_count"] == 5
    assert approved["label_value_row_count"] == 143352
    assert approved["label_family_coverage_entries"] == 144
    assert approved["available_label_value_count"] == 142200
    assert approved["unavailable_label_value_count"] == 1152
    assert approved["operator_attestation"][
        "operator_confirms_redesigned_label_profile"
    ] is True


def test_planning_approval_and_only_permitted_readiness_are_true(
    approved: dict,
) -> None:
    assert approved["feature_predictive_evidence_planning_approved"] is True
    assert approved["feature_predictive_evidence_planning_approval_created"] is True
    assert approved[
        "ready_for_feature_generation_candidate_using_redesigned_labels"
    ] is True
    assert approved[
        "ready_for_additional_predictive_evidence_execution_candidate_using_redesigned_labels"
    ] is False
    assert approved["feature_predictive_evidence_planning_objective"] == (
        "APPROVE_FEATURE_AND_PREDICTIVE_EVIDENCE_PLANNING_USING_REDESIGNED_LABELS"
    )
    assert approved["feature_predictive_evidence_planning_mode"] == (
        "APPROVED_NOT_EXECUTED"
    )
    assert approved["feature_predictive_evidence_planning_authority_status"] == (
        approval.APPROVED_FOR_FUTURE_FEATURE_GENERATION_CANDIDATE_ONLY
    )


@pytest.mark.parametrize(
    "field",
    [
        "feature_generation_candidate_created",
        "feature_generation_authorized",
        "feature_generation_performed",
        "redesigned_feature_generation_authorized",
        "redesigned_feature_generation_performed",
        "additional_predictive_evidence_execution_candidate_created",
        "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed",
        "metric_recomputation_performed",
        "model_training_performed",
        "predictive_usefulness_acceptance_ready",
        "predictive_usefulness_acceptance_recommended",
        "predictive_usefulness_acceptance_candidate_created",
        "profitability_acceptance_ready",
        "profitability_acceptance_recommended",
        "runtime_migration_approved",
        "runtime_migration_active",
        "automatic_stitching",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
    ],
)
def test_all_downstream_execution_and_authority_flags_remain_false(
    approved: dict, field: str
) -> None:
    assert approved[field] is False


@pytest.mark.parametrize(
    "field",
    ["runtime_use", "strategy_use", "paper_trading", "broker_execution"],
)
def test_runtime_and_trading_authority_remain_closed(
    approved: dict, field: str
) -> None:
    assert approved[field] == approval.NOT_AUTHORIZED


def test_predictive_usefulness_and_profitability_are_not_accepted(
    approved: dict,
) -> None:
    assert approved["predictive_usefulness"] == approval.NOT_ACCEPTED
    assert approved["profitability"] == approval.NOT_ACCEPTED


def test_approved_source_inputs_are_exact_and_planning_only(approved: dict) -> None:
    rows = approved["approved_source_inputs"]
    assert [row["source_input_id"] for row in rows] == (
        approval.review_service.candidate_service.SOURCE_INPUT_IDS
    )
    assert len(rows) == 9
    assert all(row["approval_status"] == approval.APPROVED_FOR_FUTURE_PLANNING_ONLY for row in rows)
    assert all(row["generation_status"] == approval.NOT_REGENERATED for row in rows)
    assert all(row["research_only"] is True and row["non_actionable"] is True for row in rows)


def test_approved_feature_families_are_exact_and_not_authorized(
    approved: dict,
) -> None:
    rows = approved["approved_planned_feature_families"]
    assert [row["feature_family_id"] for row in rows] == (
        approval.review_service.candidate_service.PLANNED_FEATURE_FAMILY_IDS
    )
    assert len(rows) == 10
    assert all(row["approval_status"] == approval.APPROVED_FOR_FUTURE_FEATURE_GENERATION_CANDIDATE_ONLY for row in rows)
    assert all(row["feature_generation_authorized"] is False for row in rows)
    assert all(row["feature_generation_performed"] is False for row in rows)


def test_approved_predictive_components_are_exact_and_not_executed(
    approved: dict,
) -> None:
    rows = approved["approved_planned_predictive_evidence_components"]
    assert [row["component_id"] for row in rows] == (
        approval.review_service.candidate_service.PLANNED_PREDICTIVE_COMPONENT_IDS
    )
    assert len(rows) == 10
    assert all(row["approval_status"] == approval.APPROVED_FOR_FUTURE_PLANNING_ONLY for row in rows)
    assert all(row["execution_authorized"] is False for row in rows)
    assert all(row["execution_performed"] is False for row in rows)


def test_approved_model_baseline_families_are_exact_and_not_trained(
    approved: dict,
) -> None:
    rows = approved["approved_planned_model_baseline_families"]
    assert [row["model_or_baseline_family_id"] for row in rows] == (
        approval.review_service.candidate_service.PLANNED_MODEL_BASELINE_FAMILY_IDS
    )
    assert len(rows) == 9
    assert all(row["approval_status"] == approval.APPROVED_FOR_FUTURE_PLANNING_ONLY for row in rows)
    assert all(row["training_authorized"] is False for row in rows)
    assert all(row["training_performed"] is False for row in rows)


def test_per_ticker_approval_entries_preserve_counts_and_boundaries(
    approved: dict,
) -> None:
    rows = approved["per_ticker_feature_predictive_evidence_planning_approvals"]
    assert len(rows) == 12
    assert [row["ticker"] for row in rows] == approval.TARGET_UNIVERSE
    assert len(
        {
            row["per_ticker_feature_predictive_evidence_planning_approval_digest"]
            for row in rows
        }
    ) == 12
    for row in rows:
        is_meta = row["ticker"] == "META"
        assert row["historical_record_count"] == (913 if is_meta else 1003)
        assert row["meta_reduced_record_count_flag"] is is_meta
        assert row["feature_predictive_evidence_planning_approval_status"] == (
            approval.APPROVED_FOR_FUTURE_FEATURE_GENERATION_CANDIDATE_ONLY
        )
        assert row["feature_generation_authorized"] is False
        assert row["feature_generation_performed"] is False
        assert row["predictive_evidence_execution_authorized"] is False
        assert row["predictive_evidence_execution_performed"] is False
        assert row["source_feature_predictive_evidence_planning_candidate_review_digest"] == approval.EXPECTED_CANDIDATE_REVIEW_PACKAGE_DIGEST
        assert row["source_feature_predictive_evidence_planning_candidate_digest"] == approval.EXPECTED_CANDIDATE_DIGEST
        assert row["per_ticker_feature_predictive_evidence_planning_approval_digest"] == approval.per_ticker_feature_predictive_evidence_planning_approval_digest_v1(row)
    assert next(row for row in rows if row["ticker"] == "META")["planning_note"] == (
        "PRESERVE_META_LIMITATION_IN_FEATURE_AND_PREDICTIVE_EVIDENCE_PLANNING"
    )


def test_next_chain_gates_and_risk_controls_are_exact(approved: dict) -> None:
    assert approved["next_chain"] == approval.NEXT_CHAIN
    assert len(approved["next_chain"]) == 12
    assert approved["next_gates"] == approval.NEXT_GATES
    assert len(approved["next_gates"]) == 14
    assert approved["risk_controls"] == approval.RISK_CONTROLS
    assert len(approved["risk_controls"]) == 18


def test_approval_checklist_passes_all_required_checks(approved: dict) -> None:
    assert [row["check_id"] for row in approved["approval_checklist"]] == (
        approval.REQUIRED_CHECK_IDS
    )
    assert len(approved["approval_checklist"]) == 57
    assert all(row["status"] == approval.PASS for row in approved["approval_checklist"])
    assert all(set(row) == {"check_id", "status", "expected", "actual", "severity", "message"} for row in approved["approval_checklist"])
    assert approved["approval_summary"]["total_checks"] == 57
    assert approved["approval_summary"]["passed_checks"] == 57
    assert approved["approval_summary"]["failed_checks"] == 0
    assert approved["approval_summary"]["blocker_count"] == 0


def test_approval_digest_is_deterministic(source_review: dict) -> None:
    first = _build(source_review)
    second = _build(source_review)
    assert first == second
    assert first["feature_predictive_evidence_planning_approval_using_redesigned_labels_digest"] == second["feature_predictive_evidence_planning_approval_using_redesigned_labels_digest"]
    assert first["feature_predictive_evidence_planning_approval_using_redesigned_labels_digest"] == approval.feature_predictive_evidence_planning_approval_using_redesigned_labels_digest_v1(first)


def test_per_ticker_approval_digests_are_deterministic(source_review: dict) -> None:
    first = _build(source_review)["per_ticker_feature_predictive_evidence_planning_approvals"]
    second = _build(source_review)["per_ticker_feature_predictive_evidence_planning_approvals"]
    assert [row["per_ticker_feature_predictive_evidence_planning_approval_digest"] for row in first] == [row["per_ticker_feature_predictive_evidence_planning_approval_digest"] for row in second]


def test_validator_accepts_valid_approval(
    approved: dict, source_review: dict
) -> None:
    validation = _validate(deepcopy(approved), source_review)
    assert validation["feature_predictive_evidence_planning_approved"] is True
    assert validation["ready_for_feature_generation_candidate_using_redesigned_labels"] is True
    assert validation["ready_for_additional_predictive_evidence_execution_candidate_using_redesigned_labels"] is False
    assert validation["per_ticker_approval_count"] == 12
    assert validation["blocker_count"] == 0


@pytest.mark.parametrize(
    "field,value",
    [
        ("artifact_kind", "WRONG"),
        ("approval_status", "WRONG"),
        ("approval_scope", "WRONG"),
        ("feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_package_digest", None),
        ("feature_predictive_evidence_planning_candidate_using_redesigned_labels_digest", None),
        ("redesigned_label_generation_results_review_package_digest", None),
        ("label_values_digest", None),
        ("records_digest", None),
        ("target_universe", list(reversed(approval.TARGET_UNIVERSE))),
        ("target_universe_count", 11),
        ("meta_record_count", 1003),
        ("feature_predictive_evidence_planning_approved", False),
        ("feature_predictive_evidence_planning_approval_created", False),
        ("ready_for_feature_generation_candidate_using_redesigned_labels", False),
        ("ready_for_additional_predictive_evidence_execution_candidate_using_redesigned_labels", True),
        ("feature_generation_candidate_created", True),
        ("feature_generation_authorized", True),
        ("feature_generation_performed", True),
        ("additional_predictive_evidence_execution_candidate_created", True),
        ("additional_predictive_evidence_execution_authorized", True),
        ("additional_predictive_evidence_executed", True),
        ("metric_recomputation_performed", True),
        ("model_training_performed", True),
        ("predictive_usefulness", "accepted"),
        ("profitability", "accepted"),
        ("runtime_use", "AUTHORIZED"),
        ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
        ("trade_recommendations_generated", True),
        ("risk_controls", None),
    ],
)
def test_validator_rejects_invalid_or_expanded_authority(
    approved: dict, source_review: dict, field: str, value
) -> None:
    changed = deepcopy(approved)
    changed[field] = value
    with pytest.raises(
        approval.FeaturePredictiveEvidencePlanningApprovalRedesignedLabelsError
    ):
        _validate(changed, source_review)


@pytest.mark.parametrize(
    "field,value",
    [
        ("operator_decision", "WRONG"),
        ("operator_attestation_phrase", "WRONG"),
        ("operator_confirms_feature_predictive_evidence_planning_candidate_review_digest", "0" * 64),
        ("operator_confirms_feature_predictive_evidence_planning_candidate_digest", "0" * 64),
        ("operator_confirms_redesigned_label_results_review_digest", "0" * 64),
        ("operator_confirms_redesigned_label_execution_digest", "0" * 64),
        ("operator_confirms_redesigned_label_approval_digest", "0" * 64),
        ("operator_confirms_research_registry_approval_digest", "0" * 64),
        ("operator_confirms_records_digest", "0" * 64),
        ("operator_confirms_label_values_digest", "0" * 64),
        ("operator_confirms_target_universe", list(reversed(approval.TARGET_UNIVERSE))),
        ("operator_confirms_target_count", 11),
        ("operator_confirms_meta_record_count", 1003),
        ("operator_confirms_non_meta_record_count", 913),
        ("operator_reference", ""),
        ("operator_attestation_timestamp_utc", ""),
    ],
)
def test_builder_rejects_invalid_operator_attestation(
    source_review: dict, field: str, value
) -> None:
    with pytest.raises(
        approval.FeaturePredictiveEvidencePlanningApprovalRedesignedLabelsError
    ):
        _build(source_review, _attestation(**{field: value}))


@pytest.mark.parametrize(
    "field", approval.REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS
)
def test_builder_rejects_each_missing_required_confirmation(
    source_review: dict, field: str
) -> None:
    with pytest.raises(
        approval.FeaturePredictiveEvidencePlanningApprovalRedesignedLabelsError
    ):
        _build(source_review, _attestation(**{field: False}))


@pytest.mark.parametrize(
    "field",
    [
        "approved_source_inputs",
        "approved_planned_feature_families",
        "approved_planned_predictive_evidence_components",
        "approved_planned_model_baseline_families",
        "next_chain",
        "next_gates",
        "risk_controls",
    ],
)
def test_validator_rejects_missing_required_collections(
    approved: dict, source_review: dict, field: str
) -> None:
    changed = deepcopy(approved)
    changed.pop(field)
    with pytest.raises(
        approval.FeaturePredictiveEvidencePlanningApprovalRedesignedLabelsError
    ):
        _validate(changed, source_review)


def test_validator_rejects_missing_approval_digest(
    approved: dict, source_review: dict
) -> None:
    changed = deepcopy(approved)
    changed.pop(
        "feature_predictive_evidence_planning_approval_using_redesigned_labels_digest"
    )
    with pytest.raises(
        approval.FeaturePredictiveEvidencePlanningApprovalRedesignedLabelsError
    ):
        _validate(changed, source_review)


def test_validator_rejects_missing_per_ticker_approval_digest(
    approved: dict, source_review: dict
) -> None:
    changed = deepcopy(approved)
    changed["per_ticker_feature_predictive_evidence_planning_approvals"][0].pop(
        "per_ticker_feature_predictive_evidence_planning_approval_digest"
    )
    with pytest.raises(
        approval.FeaturePredictiveEvidencePlanningApprovalRedesignedLabelsError
    ):
        _validate(changed, source_review)


def test_markdown_contains_required_sections(approved: dict, source_review: dict) -> None:
    with patch.object(
        approval, "_source_review", return_value=deepcopy(source_review)
    ):
        markdown = approval.build_feature_predictive_evidence_planning_approved_using_redesigned_labels_markdown_v1(
            approved
        )
    sections = [
        "Title",
        "Feature / Predictive Evidence Planning Approval Using Redesigned Labels",
        "Operator Attestation",
        "Bound Evidence",
        "Dataset and Universe",
        "Approved Redesigned Label Profile",
        "Approved Source Inputs",
        "Approved Feature Families",
        "Approved Predictive Evidence Components",
        "Approved Model and Baseline Families",
        "Per-Ticker Approval Entries",
        "Next Chain",
        "Next Gates",
        "Risk Controls",
        "Checklist Summary",
        "Guardrails",
    ]
    for section in sections:
        assert f"## {section}" in markdown


def test_writer_writes_canonical_approval_once(
    source_review: dict, approved: dict, tmp_path
) -> None:
    with patch.object(
        approval, "_source_review", return_value=deepcopy(source_review)
    ):
        result = approval.write_feature_predictive_evidence_planning_approved_using_redesigned_labels_v1(
            tmp_path, operator_attestation=_attestation()
        )
        written = json.loads(
            (tmp_path / result["filename"]).read_text(encoding="utf-8")
        )
        assert written == approved
        with pytest.raises(
            approval.FeaturePredictiveEvidencePlanningApprovalRedesignedLabelsError
        ):
            approval.write_feature_predictive_evidence_planning_approved_using_redesigned_labels_v1(
                tmp_path, operator_attestation=_attestation()
            )


def test_service_exports_are_available() -> None:
    assert services.build_feature_predictive_evidence_planning_approval_using_redesigned_labels_attestation_v1 is approval.build_feature_predictive_evidence_planning_approval_using_redesigned_labels_attestation_v1
    assert services.build_feature_predictive_evidence_planning_approved_using_redesigned_labels_v1 is approval.build_feature_predictive_evidence_planning_approved_using_redesigned_labels_v1
    assert services.validate_feature_predictive_evidence_planning_approved_using_redesigned_labels_v1 is approval.validate_feature_predictive_evidence_planning_approved_using_redesigned_labels_v1
    assert services.write_feature_predictive_evidence_planning_approved_using_redesigned_labels_v1 is approval.write_feature_predictive_evidence_planning_approved_using_redesigned_labels_v1
