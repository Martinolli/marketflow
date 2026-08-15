from __future__ import annotations

from copy import deepcopy
import json
from unittest.mock import patch

import pytest

from marketflow.historical_data.artifacts import canonical_json_bytes, sha256_bytes
from marketflow.services import feature_label_refinement_plan_approval_service as approval


def _attestation(**overrides) -> dict:
    kwargs = {
        "operator_reference": "TEST_OPERATOR",
        "operator_attestation_timestamp_utc": "2026-08-15T12:00:00Z",
        "operator_attestation_phrase": approval.REQUIRED_FEATURE_LABEL_REFINEMENT_PLAN_APPROVAL_ATTESTATION_PHRASE,
        "operator_confirms_target_universe": list(approval.TARGET_UNIVERSE),
        "operator_confirms_target_count": 12,
        "operator_confirms_readiness_reason": "MIXED_STABILITY_AND_INSUFFICIENT_BASELINE_OUTPERFORMANCE",
        **approval._expected_digest_confirmations(),
        **{
            name: True
            for name in approval.REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS
        },
    }
    kwargs.update(overrides)
    return approval.build_feature_label_refinement_plan_approval_attestation_v1(
        **kwargs
    )


@pytest.fixture(scope="module")
def source_review() -> dict:
    return approval.review_service.build_feature_label_refinement_plan_candidate_review_package_v1()


def _build(source_review: dict, attestation: dict | None = None) -> dict:
    with patch.object(
        approval, "_source_review", return_value=deepcopy(source_review)
    ):
        return approval.build_feature_label_refinement_plan_approved_v1(
            operator_attestation=_attestation() if attestation is None else attestation
        )


def _validate(approved: dict, source_review: dict) -> dict:
    with patch.object(
        approval, "_source_review", return_value=deepcopy(source_review)
    ):
        return approval.validate_feature_label_refinement_plan_approved_v1(approved)


@pytest.fixture(scope="module")
def approved(source_review: dict) -> dict:
    return _build(source_review)


def test_attestation_builder_creates_all_required_fields() -> None:
    attestation = _attestation()
    assert attestation["operator_decision"] == (
        approval.OPERATOR_DECISION_APPROVE_FEATURE_LABEL_REFINEMENT_PLAN
    )
    assert attestation["operator_attestation_version"] == (
        approval.OPERATOR_ATTESTATION_VERSION_FEATURE_LABEL_REFINEMENT_PLAN_APPROVAL_V1
    )
    assert attestation["operator_reference"] == "TEST_OPERATOR"
    assert attestation["operator_attestation_timestamp_utc"] == (
        "2026-08-15T12:00:00Z"
    )
    assert attestation["operator_attestation_phrase"] == (
        approval.REQUIRED_FEATURE_LABEL_REFINEMENT_PLAN_APPROVAL_ATTESTATION_PHRASE
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
    assert artifact["provider_requests_made_in_approval"] is False


def test_default_source_review_builder_path_is_supported(source_review: dict) -> None:
    validation = {
        "feature_label_refinement_plan_candidate_review_package_digest": (
            approval.EXPECTED_CANDIDATE_REVIEW_PACKAGE_DIGEST
        )
    }
    with (
        patch.object(
            approval.review_service,
            "build_feature_label_refinement_plan_candidate_review_package_v1",
            return_value=deepcopy(source_review),
        ),
        patch.object(
            approval.review_service,
            "validate_feature_label_refinement_plan_candidate_review_package_v1",
            return_value=validation,
        ),
    ):
        artifact = approval.build_feature_label_refinement_plan_approved_v1(
            operator_attestation=_attestation()
        )
    assert artifact["feature_label_refinement_plan_approved"] is True


def test_artifact_schema_status_and_scope(approved: dict) -> None:
    assert approved["artifact_kind"] == (
        approval.ARTIFACT_KIND_FEATURE_LABEL_REFINEMENT_PLAN_APPROVED
    )
    assert approved["schema_version"] == (
        approval.SCHEMA_VERSION_FEATURE_LABEL_REFINEMENT_PLAN_APPROVAL_V1
    )
    assert approved["approval_status"] == approval.FEATURE_LABEL_REFINEMENT_PLAN_APPROVED
    assert approved["approval_scope"] == (
        approval.FEATURE_LABEL_REFINEMENT_PLAN_APPROVAL_ONLY
    )


def test_plan_approval_and_future_candidate_readiness_are_true(approved: dict) -> None:
    assert approved["feature_label_refinement_plan_approved"] is True
    assert approved["feature_label_refinement_plan_approval_created"] is True
    assert approved["feature_label_refinement_plan_approved_by_operator"] is True
    assert approved["ready_for_feature_label_refinement_execution_candidate"] is True
    assert approved["feature_label_refinement_plan_scope"] == (
        approval.PLAN_APPROVAL_SCOPE
    )
    assert approved["feature_label_refinement_plan_mode"] == (
        approval.APPROVED_NOT_EXECUTED
    )
    assert approved["feature_label_refinement_plan_authority_status"] == (
        approval.APPROVED_FOR_FUTURE_EXECUTION_CANDIDATE_ONLY
    )


@pytest.mark.parametrize(
    "field,expected",
    [
        ("feature_label_refinement_plan_candidate_review_package_digest", approval.EXPECTED_CANDIDATE_REVIEW_PACKAGE_DIGEST),
        ("feature_label_refinement_plan_candidate_digest", approval.EXPECTED_CANDIDATE_DIGEST),
        ("predictive_evidence_improvement_candidate_review_package_digest", approval.EXPECTED_IMPROVEMENT_CANDIDATE_REVIEW_PACKAGE_DIGEST),
        ("predictive_evidence_improvement_candidate_digest", approval.EXPECTED_IMPROVEMENT_CANDIDATE_DIGEST),
        ("predictive_usefulness_acceptance_readiness_review_digest", approval.EXPECTED_READINESS_REVIEW_DIGEST),
        ("predictive_usefulness_reassessment_review_package_digest", approval.EXPECTED_REASSESSMENT_REVIEW_DIGEST),
        ("additional_predictive_evidence_results_review_package_digest", approval.EXPECTED_RESULTS_REVIEW_DIGEST),
        ("additional_predictive_evidence_execution_digest", approval.EXPECTED_EXECUTION_DIGEST),
        ("research_registry_approval_digest", approval.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST),
        ("canonical_dataset_freeze_digest", approval.EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST),
        ("records_digest", approval.EXPECTED_RECORDS_DIGEST),
    ],
)
def test_all_source_digests_are_bound(
    approved: dict, field: str, expected: str
) -> None:
    assert approved[field] == expected


def test_target_universe_is_exact_and_ordered(approved: dict) -> None:
    assert approved["target_universe_count"] == 12
    assert approved["target_universe"] == [
        "MSFT", "NVDA", "AMZN", "GOOGL", "META", "TSLA",
        "JPM", "XOM", "JNJ", "WMT", "CAT", "LMT",
    ]


def test_readiness_failure_basis_remains_not_ready(approved: dict) -> None:
    assert approved["readiness_failure_basis"] == {
        "stability_consistency_required": "FAIL_OR_NOT_MET",
        "baseline_outperformance_consistency_required": "FAIL_OR_NOT_MET",
        "readiness_decision": "PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY",
        "readiness_reason": "MIXED_STABILITY_AND_INSUFFICIENT_BASELINE_OUTPERFORMANCE",
    }
    assert approved["evidence_basis"] == {
        "walk_forward_accuracy_range": "0.498698 to 0.562842",
        "oos_majority_accuracy": "0.539491",
        "oos_previous_direction_accuracy": "0.495984",
        "oos_ticker_cross_sectional_accuracy": "0.502677",
        "oos_brier_score": "0.24875351",
        "leakage_status": "PASS",
        "failed_leakage_controls": 0,
    }


@pytest.mark.parametrize(
    "field,expected_ids",
    [
        ("approved_label_refinement_groups", approval.review_service.candidate_service.LABEL_REFINEMENT_GROUP_IDS),
        ("approved_feature_refinement_groups", approval.review_service.candidate_service.FEATURE_REFINEMENT_GROUP_IDS),
        ("approved_protocol_refinement_groups", approval.review_service.candidate_service.PROTOCOL_REFINEMENT_GROUP_IDS),
        ("approved_model_comparison_groups", approval.review_service.candidate_service.MODEL_COMPARISON_GROUP_IDS),
    ],
)
def test_groups_are_approved_only_for_future_execution_candidate_planning(
    approved: dict, field: str, expected_ids: list[str]
) -> None:
    groups = approved[field]
    assert [row["group_id"] for row in groups] == expected_ids
    assert all(
        row["approval_status"]
        == approval.APPROVED_FOR_FUTURE_EXECUTION_CANDIDATE_ONLY
        for row in groups
    )
    assert all(
        row["authorization_status"] == approval.NOT_AUTHORIZED_FOR_EXECUTION
        for row in groups
    )
    assert all(row["execution_status"] == approval.NOT_EXECUTED for row in groups)
    assert all(row["research_only"] is True for row in groups)
    assert all(row["non_actionable"] is True for row in groups)


def test_refinement_priority_is_preserved_as_plan_priority(approved: dict) -> None:
    assert approved["approved_refinement_priority"] == (
        approval.review_service.candidate_service.REFINEMENT_PRIORITY
    )
    assert approved["feature_label_refinement_execution_authorized"] is False


def test_per_ticker_plan_approval_entries_preserve_counts_and_digests(
    approved: dict,
) -> None:
    entries = approved["per_ticker_feature_label_refinement_plan_approvals"]
    assert len(entries) == 12
    assert [row["ticker"] for row in entries] == approval.TARGET_UNIVERSE
    assert len(
        {
            row["per_ticker_feature_label_refinement_plan_approval_digest"]
            for row in entries
        }
    ) == 12
    for row in entries:
        is_meta = row["ticker"] == "META"
        assert row["registry_approval_status"] == "APPROVED_FOR_RESEARCH_REGISTRY_ONLY"
        assert row["canonical_dataset_status"] == "FROZEN"
        assert row["historical_record_count"] == (913 if is_meta else 1003)
        assert row["meta_reduced_record_count_flag"] is is_meta
        assert row["readiness_status"] == "NOT_READY"
        assert row["feature_label_refinement_plan_status"] == (
            approval.APPROVED_FOR_FUTURE_EXECUTION_CANDIDATE_ONLY
        )
        assert row["feature_label_refinement_execution_status"] == approval.NOT_EXECUTED
        assert row["refinement_execution_authorized"] is False
        assert row["source_feature_label_refinement_plan_candidate_review_digest"] == (
            approval.EXPECTED_CANDIDATE_REVIEW_PACKAGE_DIGEST
        )
        assert row["source_feature_label_refinement_plan_candidate_digest"] == (
            approval.EXPECTED_CANDIDATE_DIGEST
        )
        assert row[
            "per_ticker_feature_label_refinement_plan_approval_digest"
        ] == approval.per_ticker_feature_label_refinement_plan_approval_digest_v1(row)
        assert row["predictive_usefulness"] == approval.NOT_ACCEPTED
        assert row["profitability"] == approval.NOT_ACCEPTED
        assert row["runtime_use"] == approval.NOT_AUTHORIZED


def test_meta_limitation_is_preserved_exactly(approved: dict) -> None:
    entries = approved["per_ticker_feature_label_refinement_plan_approvals"]
    meta = next(row for row in entries if row["ticker"] == "META")
    others = [row for row in entries if row["ticker"] != "META"]
    assert meta["refinement_note"] == (
        "PRESERVE_REDUCED_RECORD_COUNT_AND_INCLUDE_LIMITATION_FLAG_IN_FEATURE_PLAN"
    )
    assert all("refinement_note" not in row for row in others)


def test_next_chain_gates_controls_and_limitations_are_defined(approved: dict) -> None:
    assert approved["next_chain"] == approval.NEXT_CHAIN
    assert approved["next_gates"] == approval.NEXT_GATES
    assert approved["risk_controls"] == approval.RISK_CONTROLS
    assert approved["limitations"] == approval.LIMITATIONS


@pytest.mark.parametrize(
    "field,expected",
    [
        ("feature_label_refinement_authorized", False),
        ("feature_label_refinement_executed", False),
        ("feature_label_refinement_execution_candidate_created", False),
        ("feature_label_refinement_execution_authorized", False),
        ("refined_label_generation_authorized", False),
        ("refined_label_generation_performed", False),
        ("refined_feature_generation_authorized", False),
        ("refined_feature_generation_performed", False),
        ("refined_walk_forward_validation_authorized", False),
        ("refined_walk_forward_validation_performed", False),
        ("refined_out_of_sample_evaluation_authorized", False),
        ("refined_out_of_sample_evaluation_performed", False),
        ("refined_metrics_recomputation_authorized", False),
        ("refined_metrics_recomputation_performed", False),
        ("model_comparison_authorized", False),
        ("model_comparison_performed", False),
        ("additional_predictive_evidence_execution_candidate_created", False),
        ("additional_predictive_evidence_execution_authorized", False),
        ("additional_predictive_evidence_executed", False),
        ("provider_requests_made_in_approval", False),
        ("live_provider_transport_enabled_in_approval", False),
        ("market_data_acquisition_performed_in_approval", False),
        ("dataset_generation_performed_in_approval", False),
        ("canonical_dataset_regenerated_in_approval", False),
        ("predictive_execution_rerun_performed", False),
        ("label_generation_rerun_performed", False),
        ("feature_matrix_rerun_performed", False),
        ("walk_forward_validation_rerun_performed", False),
        ("out_of_sample_evaluation_rerun_performed", False),
        ("metrics_recomputation_performed", False),
        ("improvement_execution_performed", False),
        ("refinement_option_execution_performed", False),
        ("label_refinement_execution_performed", False),
        ("feature_refinement_execution_performed", False),
        ("protocol_refinement_execution_performed", False),
        ("new_strategy_scoring_performed", False),
        ("trade_recommendations_generated", False),
        ("raw_provider_payloads_committed", False),
        ("api_keys_stored_or_printed", False),
        ("predictive_usefulness", approval.NOT_ACCEPTED),
        ("predictive_usefulness_acceptance_ready", False),
        ("predictive_usefulness_acceptance_recommended", False),
        ("predictive_usefulness_acceptance_candidate_created", False),
        ("profitability", approval.NOT_ACCEPTED),
        ("profitability_acceptance_ready", False),
        ("profitability_acceptance_recommended", False),
        ("runtime_migration_approved", False),
        ("runtime_migration_active", False),
        ("runtime_use", approval.NOT_AUTHORIZED),
        ("strategy_use", approval.NOT_AUTHORIZED),
        ("paper_trading", approval.NOT_AUTHORIZED),
        ("broker_execution", approval.NOT_AUTHORIZED),
        ("automatic_stitching", False),
    ],
)
def test_execution_acceptance_and_runtime_boundaries_remain_closed(
    approved: dict, field: str, expected: object
) -> None:
    assert approved[field] == expected


def test_checklist_and_summary_are_complete(approved: dict) -> None:
    checklist = approved["approval_checklist"]
    summary = approved["approval_summary"]
    assert [row["check_id"] for row in checklist] == approval.REQUIRED_CHECK_IDS
    assert all(row["status"] == approval.PASS for row in checklist)
    assert all(set(row) == {"check_id", "status", "expected", "actual", "severity", "message"} for row in checklist)
    assert summary["total_checks"] == len(approval.REQUIRED_CHECK_IDS) == 80
    assert summary["passed_checks"] == 80
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["feature_label_refinement_plan_approved_by_operator"] is True
    assert summary["ready_for_feature_label_refinement_execution_candidate"] is True
    assert summary["feature_label_refinement_executed"] is False
    assert summary["predictive_usefulness_accepted"] is False
    assert summary["profitability_accepted"] is False
    assert summary["runtime_migration_authorized"] is False


@pytest.mark.parametrize(
    "field,value",
    [
        ("operator_decision", "WRONG"),
        ("operator_attestation_phrase", "WRONG"),
        ("operator_reference", ""),
        ("operator_attestation_timestamp_utc", ""),
        ("operator_confirms_target_universe", list(reversed(approval.TARGET_UNIVERSE))),
        ("operator_confirms_target_count", 11),
        ("operator_confirms_readiness_reason", "WRONG"),
    ],
)
def test_builder_rejects_wrong_core_attestation_fields(
    source_review: dict, field: str, value: object
) -> None:
    with pytest.raises(approval.FeatureLabelRefinementPlanApprovalError):
        _build(source_review, _attestation(**{field: value}))


@pytest.mark.parametrize(
    "field",
    list(approval._expected_digest_confirmations()),
)
def test_builder_rejects_wrong_source_digest_confirmations(
    source_review: dict, field: str
) -> None:
    with pytest.raises(approval.FeatureLabelRefinementPlanApprovalError):
        _build(source_review, _attestation(**{field: "0" * 64}))


@pytest.mark.parametrize(
    "field",
    approval.REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS,
)
def test_builder_rejects_missing_boundary_confirmations(
    source_review: dict, field: str
) -> None:
    with pytest.raises(approval.FeatureLabelRefinementPlanApprovalError):
        _build(source_review, _attestation(**{field: False}))


def test_validator_accepts_valid_approval(approved: dict, source_review: dict) -> None:
    result = _validate(approved, source_review)
    assert result["status"] == "FEATURE_LABEL_REFINEMENT_PLAN_APPROVAL_VALID"
    assert result["blocker_count"] == 0
    assert result["feature_label_refinement_plan_approved"] is True
    assert result["ready_for_feature_label_refinement_execution_candidate"] is True
    assert result["feature_label_refinement_executed"] is False
    assert result["predictive_usefulness"] == approval.NOT_ACCEPTED
    assert result["profitability"] == approval.NOT_ACCEPTED


@pytest.mark.parametrize(
    "field,value",
    [
        ("artifact_kind", "WRONG"),
        ("approval_status", "WRONG"),
        ("approval_scope", "WRONG"),
        ("feature_label_refinement_plan_approved", False),
        ("feature_label_refinement_plan_approval_created", False),
        ("ready_for_feature_label_refinement_execution_candidate", False),
        ("feature_label_refinement_authorized", True),
        ("feature_label_refinement_executed", True),
        ("feature_label_refinement_execution_candidate_created", True),
        ("feature_label_refinement_execution_authorized", True),
        ("refined_label_generation_authorized", True),
        ("refined_label_generation_performed", True),
        ("refined_feature_generation_authorized", True),
        ("refined_feature_generation_performed", True),
        ("model_comparison_authorized", True),
        ("model_comparison_performed", True),
        ("additional_predictive_evidence_execution_candidate_created", True),
        ("additional_predictive_evidence_execution_authorized", True),
        ("additional_predictive_evidence_executed", True),
        ("predictive_usefulness", "accepted"),
        ("predictive_usefulness_acceptance_ready", True),
        ("predictive_usefulness_acceptance_recommended", True),
        ("predictive_usefulness_acceptance_candidate_created", True),
        ("profitability", "accepted"),
        ("profitability_acceptance_ready", True),
        ("profitability_acceptance_recommended", True),
        ("runtime_migration_approved", True),
        ("runtime_use", "AUTHORIZED"),
        ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
        ("automatic_stitching", True),
        ("predictive_execution_rerun_performed", True),
        ("label_generation_rerun_performed", True),
        ("feature_matrix_rerun_performed", True),
        ("walk_forward_validation_rerun_performed", True),
        ("out_of_sample_evaluation_rerun_performed", True),
        ("metrics_recomputation_performed", True),
        ("improvement_execution_performed", True),
        ("refinement_option_execution_performed", True),
        ("label_refinement_execution_performed", True),
        ("feature_refinement_execution_performed", True),
        ("protocol_refinement_execution_performed", True),
        ("new_strategy_scoring_performed", True),
        ("trade_recommendations_generated", True),
        ("provider_requests_made_in_approval", True),
        ("live_provider_transport_enabled_in_approval", True),
        ("market_data_acquisition_performed_in_approval", True),
        ("raw_provider_payloads_committed", True),
        ("api_keys_stored_or_printed", True),
    ],
)
def test_validator_rejects_forbidden_mutations(
    approved: dict, source_review: dict, field: str, value: object
) -> None:
    invalid = deepcopy(approved)
    invalid[field] = value
    with pytest.raises(approval.FeatureLabelRefinementPlanApprovalError):
        _validate(invalid, source_review)


def test_validator_rejects_target_universe_mismatch(
    approved: dict, source_review: dict
) -> None:
    invalid = deepcopy(approved)
    invalid["target_universe"] = list(reversed(invalid["target_universe"]))
    with pytest.raises(approval.FeatureLabelRefinementPlanApprovalError):
        _validate(invalid, source_review)


def test_validator_rejects_readiness_decision_change(
    approved: dict, source_review: dict
) -> None:
    invalid = deepcopy(approved)
    invalid["readiness_failure_basis"]["readiness_decision"] = (
        "PREDICTIVE_USEFULNESS_ACCEPTANCE_READY"
    )
    with pytest.raises(approval.FeatureLabelRefinementPlanApprovalError):
        _validate(invalid, source_review)


def test_validator_rejects_readiness_reason_change(
    approved: dict, source_review: dict
) -> None:
    invalid = deepcopy(approved)
    invalid["readiness_failure_basis"]["readiness_reason"] = "WRONG"
    with pytest.raises(approval.FeatureLabelRefinementPlanApprovalError):
        _validate(invalid, source_review)


def test_validator_rejects_missing_approval_digest(
    approved: dict, source_review: dict
) -> None:
    invalid = deepcopy(approved)
    invalid.pop("feature_label_refinement_plan_approval_digest")
    with pytest.raises(approval.FeatureLabelRefinementPlanApprovalError):
        _validate(invalid, source_review)


def test_validator_rejects_missing_per_ticker_approval_digest(
    approved: dict, source_review: dict
) -> None:
    invalid = deepcopy(approved)
    invalid["per_ticker_feature_label_refinement_plan_approvals"][0].pop(
        "per_ticker_feature_label_refinement_plan_approval_digest"
    )
    with pytest.raises(approval.FeatureLabelRefinementPlanApprovalError):
        _validate(invalid, source_review)


def test_approval_digest_is_deterministic(approved: dict, source_review: dict) -> None:
    rebuilt = _build(source_review)
    assert rebuilt["feature_label_refinement_plan_approval_digest"] == approved[
        "feature_label_refinement_plan_approval_digest"
    ]
    assert approved["feature_label_refinement_plan_approval_digest"] == (
        approval.feature_label_refinement_plan_approval_digest_v1(approved)
    )


def test_per_ticker_approval_digests_are_deterministic(
    approved: dict, source_review: dict
) -> None:
    rebuilt = _build(source_review)
    assert [
        row["per_ticker_feature_label_refinement_plan_approval_digest"]
        for row in rebuilt["per_ticker_feature_label_refinement_plan_approvals"]
    ] == [
        row["per_ticker_feature_label_refinement_plan_approval_digest"]
        for row in approved["per_ticker_feature_label_refinement_plan_approvals"]
    ]


def test_markdown_builder_includes_required_sections(
    approved: dict, source_review: dict
) -> None:
    with patch.object(
        approval, "_source_review", return_value=deepcopy(source_review)
    ):
        markdown = approval.build_feature_label_refinement_plan_approved_markdown_v1(
            approved
        )
    for heading in (
        "# MarketFlow Feature/Label Refinement Plan Approval Status",
        "## Title",
        "## Approved Feature/Label Refinement Plan",
        "## Operator Attestation",
        "## Source Candidate Review",
        "## Readiness Failure Basis",
        "## Approved Label Refinement Groups",
        "## Approved Feature Refinement Groups",
        "## Approved Protocol Refinement Groups",
        "## Approved Model Comparison Groups",
        "## Refinement Priority",
        "## Per-Ticker Plan Approval Entries",
        "## Execution Boundary",
        "## Predictive Usefulness Boundary",
        "## Profitability Boundary",
        "## Runtime Boundary",
        "## Checklist Summary",
        "## Remaining Required Tasks",
        "## Guardrails",
    ):
        assert heading in markdown


def test_writer_emits_canonical_json_in_isolated_directory(
    tmp_path, source_review: dict
) -> None:
    with patch.object(
        approval, "_source_review", return_value=deepcopy(source_review)
    ):
        result = approval.write_feature_label_refinement_plan_approved_v1(
            tmp_path, operator_attestation=_attestation()
        )
    output = tmp_path / result["filename"]
    payload = output.read_bytes()
    written = json.loads(payload)
    assert payload == canonical_json_bytes(written)
    assert result["payload_byte_size"] == len(payload)
    assert result["payload_sha256"] == sha256_bytes(payload)
    assert result["feature_label_refinement_plan_approval_digest"] == written[
        "feature_label_refinement_plan_approval_digest"
    ]


def test_writer_refuses_overwrite(tmp_path, source_review: dict) -> None:
    with patch.object(
        approval, "_source_review", return_value=deepcopy(source_review)
    ):
        approval.write_feature_label_refinement_plan_approved_v1(
            tmp_path, operator_attestation=_attestation()
        )
        with pytest.raises(approval.FeatureLabelRefinementPlanApprovalError):
            approval.write_feature_label_refinement_plan_approved_v1(
                tmp_path, operator_attestation=_attestation()
            )


@pytest.mark.parametrize("filename", ["../approval.json", "approval.txt"])
def test_writer_rejects_unsafe_or_non_json_filename(
    tmp_path, source_review: dict, filename: str
) -> None:
    with patch.object(
        approval, "_source_review", return_value=deepcopy(source_review)
    ):
        with pytest.raises(approval.FeatureLabelRefinementPlanApprovalError):
            approval.write_feature_label_refinement_plan_approved_v1(
                tmp_path,
                operator_attestation=_attestation(),
                filename=filename,
            )
